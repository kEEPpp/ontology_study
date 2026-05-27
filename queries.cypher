// ═══════════════════════════════════════════════════════════════
// 온톨로지 실습용 Cypher 쿼리 모음
// Neo4j Browser (http://localhost:7474) 에서 하나씩 실행해보세요
// import_to_neo4j.py 실행 후 사용 가능
// ═══════════════════════════════════════════════════════════════


// ──────────────────────────────────────────────────────────────
// LEVEL 1. 기본 조회 — 온톨로지가 제대로 들어갔는지 확인
// ──────────────────────────────────────────────────────────────

// [1-1] 전체 노드 수 확인
MATCH (n:OntologyNode)
RETURN count(n) AS 총_노드수;

// [1-2] 시맨틱 스페이스별 노드 수 (9가지가 다 보여야 함)
MATCH (n:OntologyNode)
RETURN n.space AS 스페이스, count(n) AS 노드수
ORDER BY 노드수 DESC;

// [1-3] 전체 관계(엣지) 수 확인
MATCH ()-[r]->()
RETURN count(r) AS 총_관계수;

// [1-4] 전체 관계 타입 목록
MATCH ()-[r]->()
RETURN DISTINCT type(r) AS 관계타입, count(r) AS 개수
ORDER BY 개수 DESC;


// ──────────────────────────────────────────────────────────────
// LEVEL 2. 특정 노드 탐색 — 관계 따라가기
// ──────────────────────────────────────────────────────────────

// [2-1] Python 노드와 직접 연결된 모든 것 (시각화 추천)
MATCH (n:OntologyNode {id: 'subj_python'})-[r]-(m)
RETURN n, r, m;

// [2-2] Python에서 나가는 관계만 (방향 있음)
MATCH (n:OntologyNode {id: 'subj_python'})-[r]->(m)
RETURN m.label AS 연결대상, type(r) AS 관계, m.space AS 스페이스;

// [2-3] Python으로 들어오는 관계 (무엇이 Python을 참조하나?)
MATCH (m)-[r]->(n:OntologyNode {id: 'subj_python'})
RETURN m.label AS 출발노드, type(r) AS 관계, m.space AS 스페이스;

// [2-4] ML 개념과 관련된 모든 것 (2단계 깊이까지)
MATCH path = (n:OntologyNode {id: 'con_ml'})-[*1..2]-(m)
RETURN path;


// ──────────────────────────────────────────────────────────────
// LEVEL 3. 시맨틱 스페이스별 탐색
// ──────────────────────────────────────────────────────────────

// [3-1] 모든 Subject 노드 (행위자/개체)
MATCH (n:OntologyNode {space: 'Subject'})
RETURN n.id, n.label, n.created_year, n.typing
ORDER BY n.created_year;

// [3-2] 모든 Claim과 신뢰도
MATCH (n:OntologyNode {space: 'Claim'})
RETURN n.label AS 주장, n.confidence AS 신뢰도
ORDER BY n.confidence DESC;

// [3-3] Claim → Evidence 연결 (근거 추적)
MATCH (c:OntologyNode {space: 'Claim'})-[r:SUPPORTED_BY]->(e:OntologyNode {space: 'Evidence'})
RETURN c.label AS 주장, e.label AS 근거, e.source AS 출처;

// [3-4] Intensity 점수 랭킹
MATCH (n:OntologyNode {space: 'Intensity'})
RETURN n.label AS 항목, n.score AS 점수, n.description AS 설명
ORDER BY n.score DESC;

// [3-5] Policy 노드와 그것을 따르는 Subject
MATCH (s:OntologyNode {space: 'Subject'})-[:GOVERNED_BY]->(p:OntologyNode {space: 'Policy'})
RETURN s.label AS 언어, p.label AS 정책;


// ──────────────────────────────────────────────────────────────
// LEVEL 4. 경로 탐색 — 두 노드 사이의 관계 찾기
// ──────────────────────────────────────────────────────────────

// [4-1] Python과 ML 사이의 모든 경로
MATCH path = shortestPath(
  (a:OntologyNode {id: 'subj_python'})-[*]-(b:OntologyNode {id: 'con_ml'})
)
RETURN path;

// [4-2] JavaScript → 웹개발 경로 (중간 노드 포함)
MATCH path = (a:OntologyNode {id: 'subj_javascript'})-[*1..3]->(b:OntologyNode {id: 'con_web_dev'})
RETURN path;

// [4-3] 특정 관계 타입으로만 연결된 경로
MATCH (a:OntologyNode)-[:BUILT_WITH]->(b:OntologyNode)
RETURN a.label AS 프레임워크, b.label AS 기반언어;


// ──────────────────────────────────────────────────────────────
// LEVEL 5. 집계 / 분석 쿼리
// ──────────────────────────────────────────────────────────────

// [5-1] 가장 많이 참조되는 노드 (중심성 — 많이 연결될수록 핵심)
MATCH (n:OntologyNode)-[r]-()
RETURN n.label AS 노드, n.space AS 스페이스, count(r) AS 연결수
ORDER BY 연결수 DESC
LIMIT 10;

// [5-2] 관계가 없는 고립 노드 (품질 체크)
MATCH (n:OntologyNode)
WHERE NOT (n)-[]-()
RETURN n.id AS 고립노드, n.label;

// [5-3] 언어(Subject) → 사용 가능한 프레임워크(Resource) 목록
MATCH (r:OntologyNode {space: 'Resource'})-[:BUILT_WITH]->(s:OntologyNode {space: 'Subject'})
RETURN s.label AS 언어, collect(r.label) AS 프레임워크목록;

// [5-4] Claim 신뢰도 가중 평균
MATCH (n:OntologyNode {space: 'Claim'})
RETURN avg(n.confidence) AS 평균신뢰도, min(n.confidence) AS 최소, max(n.confidence) AS 최대;


// ──────────────────────────────────────────────────────────────
// LEVEL 6. 데이터 수정 — 온톨로지 업데이트 실습
// ──────────────────────────────────────────────────────────────

// [6-1] 새 노드 추가 (Go 언어)
CREATE (n:OntologyNode {
  id: 'subj_go',
  label: 'Go',
  type: 'Subject',
  space: 'Subject',
  created_year: 2009,
  creator: 'Google',
  typing: 'static',
  description: 'Google이 만든 정적 타입 컴파일 언어. 동시성 처리에 강점'
});

// [6-2] 새 관계 추가 (Go는 백엔드 웹개발에 강함)
MATCH (go:OntologyNode {id: 'subj_go'})
MATCH (web:OntologyNode {id: 'con_web_dev'})
CREATE (go)-[:EXCELS_AT {strength: 0.85, role: 'backend'}]->(web);

// [6-3] 노드 속성 업데이트
MATCH (n:OntologyNode {id: 'subj_python'})
SET n.current_version = '3.12'
RETURN n;

// [6-4] 추가한 Go 노드 확인
MATCH (n:OntologyNode {id: 'subj_go'})-[r]-(m)
RETURN n, r, m;


// ──────────────────────────────────────────────────────────────
// LEVEL 7. 전체 그래프 시각화 (Neo4j Browser 권장)
// ──────────────────────────────────────────────────────────────

// [7-1] 전체 그래프 (노드 많으면 느릴 수 있음 — LIMIT 권장)
MATCH (n:OntologyNode)-[r]-(m)
RETURN n, r, m
LIMIT 100;

// [7-2] Subject ↔ Resource 관계만 시각화
MATCH (s:OntologyNode {space: 'Subject'})-[r]-(res:OntologyNode {space: 'Resource'})
RETURN s, r, res;

// [7-3] Claim ↔ Evidence 관계만 시각화
MATCH (c:OntologyNode {space: 'Claim'})-[r]-(e:OntologyNode {space: 'Evidence'})
RETURN c, r, e;
