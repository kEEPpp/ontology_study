"""
온톨로지 샘플 팩 탐색 스크립트
- 외부 라이브러리 없이 Python 기본 모듈만 사용
- 실행: python explore.py
"""

import json, sys, io
from pathlib import Path
from collections import defaultdict

# Windows 한국어 환경 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = Path(__file__).parent / "sample_pack"

# ── 데이터 로드 ────────────────────────────────────────────────
def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

nodes = load_jsonl(BASE / "graph/nodes.jsonl")
edges = load_jsonl(BASE / "graph/edges.jsonl")
docs  = load_jsonl(BASE / "cloud/documents.jsonl")
chunks= load_jsonl(BASE / "cloud/chunks.jsonl")

node_map = {n["id"]: n for n in nodes}   # id → node 빠른 조회용

# ══════════════════════════════════════════════════════════════
# 메뉴 함수들
# ══════════════════════════════════════════════════════════════

def show_stats():
    """전체 통계"""
    print("\n" + "="*50)
    print("📊 팩 통계")
    print("="*50)
    print(f"  노드(nodes)   : {len(nodes)}개")
    print(f"  엣지(edges)   : {len(edges)}개")
    print(f"  문서(docs)    : {len(docs)}개")
    print(f"  청크(chunks)  : {len(chunks)}개")

    space_count = defaultdict(int)
    for n in nodes:
        space_count[n.get("space", "??")] += 1

    print("\n  시맨틱 스페이스별 노드 수:")
    spaces_order = ["Subject","Resource","Evidence","Concept",
                    "Result","Claim","Community","Policy","Intensity"]
    emoji = {"Subject":"👤","Resource":"📦","Evidence":"🔍","Concept":"💡",
             "Result":"🏆","Claim":"💬","Community":"👥","Policy":"📋","Intensity":"⚡"}
    for sp in spaces_order:
        cnt = space_count.get(sp, 0)
        bar = "█" * cnt
        print(f"    {emoji.get(sp,'  ')} {sp:<12} {bar} ({cnt})")


def list_nodes_by_space():
    """시맨틱 스페이스별 노드 목록"""
    space = input("\n  조회할 스페이스 이름 입력\n"
                  "  (Subject/Resource/Evidence/Concept/Result/Claim/Community/Policy/Intensity): ").strip()
    matched = [n for n in nodes if n.get("space","").lower() == space.lower()]
    if not matched:
        print(f"  '{space}' 스페이스에 해당하는 노드가 없습니다.")
        return
    print(f"\n  [{space}] 노드 {len(matched)}개:")
    for n in matched:
        desc = n.get("properties", {}).get("description", "")
        print(f"    • {n['id']:<30} {n['label']}")
        if desc:
            print(f"      └ {desc[:60]}{'...' if len(desc)>60 else ''}")


def find_connections():
    """특정 노드의 연결 관계 조회"""
    print("\n  사용 가능한 노드 ID 예시:")
    for n in nodes[:8]:
        print(f"    {n['id']}")
    node_id = input("\n  조회할 노드 ID 입력: ").strip()

    if node_id not in node_map:
        print(f"  '{node_id}' 노드를 찾을 수 없습니다.")
        return

    node = node_map[node_id]
    print(f"\n  🔵 노드: [{node['space']}] {node['label']}")
    props = node.get("properties", {})
    for k, v in props.items():
        print(f"    {k}: {v}")

    out_edges = [e for e in edges if e["source"] == node_id]
    in_edges  = [e for e in edges if e["target"] == node_id]

    print(f"\n  ▶ 나가는 관계 ({len(out_edges)}개):")
    for e in out_edges:
        tgt = node_map.get(e["target"], {})
        print(f"    → [{e['relation']}] {e['target']} ({tgt.get('label','')})")

    print(f"\n  ◀ 들어오는 관계 ({len(in_edges)}개):")
    for e in in_edges:
        src = node_map.get(e["source"], {})
        print(f"    ← [{e['relation']}] {e['source']} ({src.get('label','')})")


def search_by_keyword():
    """키워드로 노드/문서 검색"""
    kw = input("\n  검색 키워드: ").strip().lower()

    print(f"\n  🔍 '{kw}' 검색 결과:")
    hit = False

    for n in nodes:
        label = n.get("label","").lower()
        desc  = str(n.get("properties",{})).lower()
        if kw in label or kw in desc:
            print(f"    [NODE] [{n['space']}] {n['id']} — {n['label']}")
            hit = True

    for d in docs:
        if kw in d.get("title","").lower() or kw in d.get("content","").lower():
            print(f"    [DOC]  {d['id']} — {d['title']}")
            hit = True

    if not hit:
        print("  검색 결과 없음")


def trace_claim():
    """Claim → Evidence 추적 (근거 확인)"""
    claims = [n for n in nodes if n["space"] == "Claim"]
    print("\n  📋 Claim 노드 목록:")
    for i, c in enumerate(claims):
        print(f"    [{i}] {c['id']} — {c['label']}")

    idx = input("\n  번호 선택: ").strip()
    try:
        claim = claims[int(idx)]
    except (ValueError, IndexError):
        print("  잘못된 입력")
        return

    print(f"\n  💬 Claim: {claim['label']}")
    conf = claim.get("properties",{}).get("confidence","?")
    basis= claim.get("properties",{}).get("basis","")
    print(f"    신뢰도: {conf}")
    if basis:
        print(f"    근거: {basis}")

    evidences = [e for e in edges
                 if e["source"] == claim["id"] and e["relation"] == "SUPPORTED_BY"]
    print(f"\n  🔍 지지하는 Evidence ({len(evidences)}개):")
    for e in evidences:
        ev = node_map.get(e["target"], {})
        props = ev.get("properties", {})
        print(f"    • {ev.get('label','')}")
        if "source" in props:
            print(f"      출처: {props['source']}")
        if "data" in props:
            print(f"      데이터: {props['data']}")


def show_intensity_ranking():
    """Intensity 점수 랭킹"""
    intensities = [n for n in nodes if n["space"] == "Intensity"]
    intensities.sort(key=lambda n: n.get("properties",{}).get("score",0), reverse=True)

    print("\n  ⚡ Intensity 랭킹:")
    for n in intensities:
        score = n.get("properties",{}).get("score", 0)
        desc  = n.get("properties",{}).get("description","")
        bar   = "█" * int(score * 20)
        print(f"    {score:.2f} {bar}")
        print(f"         {n['label']}")
        print(f"         └ {desc}")


def export_simple_graph():
    """그래프를 간단한 텍스트로 출력"""
    print("\n  🗺️ 그래프 관계 전체 (source → relation → target):")
    relation_groups = defaultdict(list)
    for e in edges:
        relation_groups[e["relation"]].append(e)

    for rel, rel_edges in sorted(relation_groups.items()):
        print(f"\n  [{rel}] — {len(rel_edges)}개")
        for e in rel_edges:
            src_label = node_map.get(e["source"],{}).get("label", e["source"])
            tgt_label = node_map.get(e["target"],{}).get("label", e["target"])
            print(f"    {src_label} → {tgt_label}")


# ══════════════════════════════════════════════════════════════
# 메인 메뉴
# ══════════════════════════════════════════════════════════════

MENU = {
    "1": ("전체 통계 보기",          show_stats),
    "2": ("스페이스별 노드 목록",     list_nodes_by_space),
    "3": ("노드 연결 관계 조회",      find_connections),
    "4": ("키워드 검색",             search_by_keyword),
    "5": ("Claim → Evidence 추적",   trace_claim),
    "6": ("Intensity 점수 랭킹",      show_intensity_ranking),
    "7": ("전체 그래프 관계 출력",    export_simple_graph),
}

if __name__ == "__main__":
    print("\n🦀 온톨로지 샘플 팩 탐색기")
    print("  주제: 프로그래밍 언어 생태계")
    show_stats()

    while True:
        print("\n" + "─"*40)
        print("메뉴:")
        for k, (label, _) in MENU.items():
            print(f"  {k}. {label}")
        print("  q. 종료")
        choice = input("\n선택: ").strip().lower()
        if choice == "q":
            print("종료합니다.")
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print("잘못된 입력입니다.")
