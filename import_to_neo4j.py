"""
Neo4j 로컬 임포트 스크립트
- sample_pack의 nodes.jsonl / edges.jsonl → Neo4j 로컬 DB에 적재
- 실행 전 필요: pip install neo4j
- Neo4j Desktop 또는 Docker 실행 상태여야 함

사용법:
  python import_to_neo4j.py

Neo4j 연결 기본값:
  URL      : bolt://localhost:7687
  User     : neo4j
  Password : password  ← 본인 설정값으로 변경
"""

import json, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── 설정 (본인 환경에 맞게 수정) ───────────────────────────────
NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "password"   # ← 여기만 변경

BASE = Path(__file__).parent / "sample_pack"
NODES_FILE = BASE / "graph/nodes.jsonl"
EDGES_FILE = BASE / "graph/edges.jsonl"
# ─────────────────────────────────────────────────────────────


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def import_data(driver):
    nodes = load_jsonl(NODES_FILE)
    edges = load_jsonl(EDGES_FILE)

    with driver.session() as session:

        # 1. 기존 데이터 초기화 (재실행 시 중복 방지)
        print("  기존 데이터 초기화...")
        session.run("MATCH (n:OntologyNode) DETACH DELETE n")

        # 2. 노드 생성
        print(f"  노드 {len(nodes)}개 생성 중...")
        for node in nodes:
            props = node.get("properties", {})
            # 리스트 값은 Neo4j에서 string으로 변환
            clean_props = {}
            for k, v in props.items():
                clean_props[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v

            session.run(
                """
                CREATE (n:OntologyNode {
                    id:    $id,
                    label: $label,
                    type:  $type,
                    space: $space
                })
                SET n += $props
                """,
                id=node["id"],
                label=node["label"],
                type=node.get("type", ""),
                space=node.get("space", ""),
                props=clean_props,
            )

        # 3. id 인덱스 생성 (조회 속도 향상)
        print("  인덱스 생성...")
        session.run("CREATE INDEX node_id IF NOT EXISTS FOR (n:OntologyNode) ON (n.id)")

        # 4. 엣지(관계) 생성
        print(f"  엣지 {len(edges)}개 생성 중...")
        fail = 0
        for edge in edges:
            try:
                rel_type = edge["relation"].replace("-", "_").replace(" ", "_")
                result = session.run(
                    f"""
                    MATCH (a:OntologyNode {{id: $src}})
                    MATCH (b:OntologyNode {{id: $tgt}})
                    CREATE (a)-[r:{rel_type}]->(b)
                    SET r += $props
                    RETURN r
                    """,
                    src=edge["source"],
                    tgt=edge["target"],
                    props=edge.get("properties", {}),
                )
                if not result.single():
                    print(f"    [경고] 노드 없음: {edge['source']} → {edge['target']}")
                    fail += 1
            except Exception as e:
                print(f"    [오류] {edge}: {e}")
                fail += 1

        print(f"\n  완료! (실패: {fail}개)")


def verify(driver):
    """임포트 결과 검증"""
    with driver.session() as session:
        node_count = session.run("MATCH (n:OntologyNode) RETURN count(n) AS cnt").single()["cnt"]
        rel_count  = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt").single()["cnt"]

        spaces = session.run(
            "MATCH (n:OntologyNode) RETURN n.space AS space, count(n) AS cnt ORDER BY cnt DESC"
        )

        print(f"\n  검증 결과:")
        print(f"    노드 수: {node_count}")
        print(f"    관계 수: {rel_count}")
        print(f"\n  스페이스별 노드:")
        for row in spaces:
            bar = "=" * row["cnt"]
            print(f"    {row['space']:<14} {bar} ({row['cnt']})")


if __name__ == "__main__":
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("\n[오류] neo4j 패키지가 없습니다.")
        print("  설치: pip install neo4j")
        sys.exit(1)

    print(f"\nNeo4j 연결 중: {NEO4J_URI}")
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity()
        print("  연결 성공!\n")
    except Exception as e:
        print(f"  연결 실패: {e}")
        print("\n  확인사항:")
        print("  - Neo4j Desktop 또는 Docker가 실행 중인가?")
        print("  - 비밀번호가 맞는가? (이 파일 상단 NEO4J_PASSWORD 수정)")
        sys.exit(1)

    print("데이터 임포트 시작...")
    import_data(driver)
    verify(driver)
    driver.close()

    print("\n완료! 이제 http://localhost:7474 에서 그래프를 시각화할 수 있습니다.")
    print("queries.cypher 파일을 참고해서 Cypher 쿼리를 실행해보세요.")
