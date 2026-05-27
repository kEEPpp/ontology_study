# 🦀 온톨로지 실습용 샘플 팩 — "프로그래밍 언어 생태계"

> 이 샘플은 OpenCrab ZIP Pack 형식을 실제로 익히기 위한 연습용 데이터셋입니다.

---

## 📁 폴더 구조

```
sample_pack/
├── cloud/
│   ├── documents.jsonl    ← 원본 문서 (5개)
│   └── chunks.jsonl       ← 문장 단위 청크 (24개)
├── graph/
│   ├── nodes.jsonl        ← 온톨로지 노드 (34개)
│   └── edges.jsonl        ← 노드 간 관계 엣지 (48개)
└── README.md              ← 이 파일
```

---

## 🗂️ 9가지 시맨틱 스페이스 — 이 팩에서 어떻게 사용됐나?

| 스페이스 | 이 팩의 예시 | 노드 ID 예시 |
|---------|------------|------------|
| **Subject (주체)** | Python, JavaScript, Java, TypeScript, Rust | `subj_python` |
| **Resource (리소스)** | Django, FastAPI, React, TensorFlow, PyTorch | `res_django` |
| **Evidence (증거)** | TIOBE Index 2024, Stack Overflow 설문 2023 | `evd_tiobe_2024` |
| **Concept (개념)** | 객체지향(OOP), 함수형, 타입시스템, ML, 웹개발 | `con_oop` |
| **Result (결과)** | Python GitHub 1위 달성, TypeScript 도입 급증 | `res_python_popularity` |
| **Claim (클레임)** | "Python은 AI/ML 표준 언어", "JS는 웹 필수" | `claim_python_ai` |
| **Community (커뮤니티)** | PyPI, npm, Python Software Foundation | `com_pypi` |
| **Policy (정책)** | PEP 8, ECMAScript 표준, SemVer | `pol_pep8` |
| **Intensity (강도)** | Python-ML 친화도(0.95), JS 웹 지배력(0.99) | `int_python_ml_affinity` |

---

## 🔗 엣지 관계 종류 (Relation Types)

| 관계 | 설명 | 예시 |
|------|------|------|
| `EXCELS_AT` | 특화/강점 | Python → ML |
| `SUPPORTS` | 지원/호환 | Python → 웹개발 |
| `BUILT_WITH` | ~로 만들어짐 | Django → Python |
| `USED_FOR` | 사용 목적 | TensorFlow → ML |
| `EXTENDS` | 확장 | Next.js → React |
| `IS_SUPERSET_OF` | 상위호환 | TypeScript → JavaScript |
| `ACHIEVED` | 달성한 결과 | Python → 1위 |
| `SUPPORTED_BY` | 근거/증거 | Claim → Evidence |
| `GOVERNED_BY` | 규칙 적용 | Python → PEP 8 |
| `HAS_ECOSYSTEM` | 생태계 보유 | Python → PyPI |
| `MEASURES_AFFINITY_OF` | 친화도 측정 | Intensity → Subject |
| `DEPENDENCY_OF` | 의존성 | NumPy → TensorFlow |

---

## 🚀 OpenCrab에 업로드하는 방법

### Step 1 — ZIP 파일 만들기

**PowerShell (Windows):**
```powershell
# sample_pack 폴더로 이동
cd "c:\Users\HYKP\Vscode\04 Study\Ontology"

# ZIP으로 압축 (cloud/, graph/ 폴더 구조 유지)
Compress-Archive -Path ".\sample_pack\cloud", ".\sample_pack\graph" -DestinationPath ".\programming_lang_pack.zip"
```

**또는 탐색기에서:**
1. `sample_pack` 폴더 열기
2. `cloud` 폴더 + `graph` 폴더 선택
3. 우클릭 → "압축(ZIP 파일)"

> ⚠️ 주의: `sample_pack` 폴더 자체가 아니라, `cloud/`와 `graph/` 폴더를 ZIP 최상단에 위치시켜야 합니다

### Step 2 — OpenCrab 웹에서 업로드

1. [https://opencrab.sh/](https://opencrab.sh/) 접속 및 로그인
2. **Ingest 탭** 이동
3. **Data ZIP 업로드** → `programming_lang_pack.zip` 선택
4. 인제스트 히스토리에서 **"Create Pack"** 클릭
5. 팩 이름: `프로그래밍언어_생태계` (또는 원하는 이름)
6. **"Save Pack"** → 완료!

### Step 3 — MCP로 AI와 연결

```
대시보드 → MCP 탭 → URL 복사
→ Claude Code / Cursor / GPT 등에 Remote MCP로 등록
```

**연결 후 테스트 질문 예시:**
```
- "Python이 ML에 적합한 이유는 뭐야?"
- "TypeScript를 써야 하는 상황은 언제야?"
- "React와 Next.js의 차이는?"
- "TensorFlow와 PyTorch를 비교해줘"
- "웹 개발에 관련된 모든 노드를 보여줘"
```

---

## 📊 이 팩의 구성 통계

| 항목 | 수량 |
|------|------|
| 문서(documents) | 5개 |
| 청크(chunks) | 24개 |
| 노드(nodes) | 34개 |
| 엣지(edges) | 48개 |
| 커버된 시맨틱 스페이스 | 9개 전부 |
| 커버된 언어 | Python, JavaScript, TypeScript, Java, Rust |

---

## 🔍 직접 확인해보기 (Neo4j 사용 시)

LocalCrab + Neo4j가 설치되어 있다면 아래 Cypher 쿼리로 확인 가능:

```cypher
-- Python과 연결된 모든 노드 보기
MATCH (n)-[r]-(m) WHERE n.id = 'subj_python' RETURN n, r, m

-- ML 관련 노드만 보기
MATCH (n) WHERE n.space = 'Concept' AND n.label CONTAINS 'ML' RETURN n

-- Claim 노드와 근거(Evidence) 관계 보기
MATCH (c:Claim)-[r:SUPPORTED_BY]->(e:Evidence) RETURN c, r, e

-- 강도(Intensity) 점수가 0.9 이상인 노드
MATCH (i) WHERE i.space = 'Intensity' AND i.properties.score >= 0.9 RETURN i
```

---

## 💡 이 샘플로 다음을 연습할 수 있어요

- [x] ZIP Pack 파일 구조 이해
- [x] 9가지 시맨틱 스페이스 실제 적용
- [x] 노드(nodes) JSONL 형식 작성
- [x] 엣지(edges) JSONL 형식 작성
- [x] 청크(chunks) 문장 단위 분리
- [x] 문서-청크-노드 연결 (node_refs)
- [x] Claim ↔ Evidence 연결 구조
- [x] Intensity 수치화 표현

---

## 🔧 이 팩을 확장하는 아이디어

1. **노드 추가**: Go, Kotlin, Swift 등 다른 언어 추가
2. **문서 추가**: 공식 문서 URL 인제스트
3. **클레임 추가**: "Rust가 가장 안전한 언어" + 근거 Evidence
4. **커뮤니티 추가**: Reddit r/Python, Stack Overflow Python 태그
5. **정책 추가**: Python 버전 지원 정책 (Python 3.8 EOL 등)
