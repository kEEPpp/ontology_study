# 🦀 Ontology Study — 온톨로지 독학 저장소

> **이 저장소의 목적**: 온톨로지가 무엇인지 개념을 익히고,  
> 직접 데이터를 설계·구축·조회·AI 연결까지 해보는 실습 공간  
> OpenCrab은 참고 프레임워크로만 활용 — 모든 실습은 로컬에서 독립 동작

---

## 📂 파일 구성 및 목적

### 📖 문서 파일 (MD) — 읽는 순서대로 번호가 붙어있음

| 파일 | 목적 | 언제 읽나 |
|------|------|----------|
| **[01_개념학습_OpenCrab_스터디가이드.md](01_개념학습_OpenCrab_스터디가이드.md)** | 온톨로지가 무엇인지, 9가지 시맨틱 스페이스, 핵심 용어, 링크 25개+ | 아무것도 모를 때 **가장 먼저** |
| **[02_실습흐름도_전체구성.md](02_실습흐름도_전체구성.md)** | 이 저장소의 전체 학습 경로 지도. 어디서 시작할지 모를 때 | 개념 파악 후 **방향 잡을 때** |
| **[03_로컬스크립트_단계별_실습가이드.md](03_로컬스크립트_단계별_실습가이드.md)** | explore.py / Neo4j / ai_context.py 단계별 사용법 + 체크리스트 | **실제 손으로 해볼 때** |
| **[sample_pack/샘플팩_데이터구조_설명.md](sample_pack/샘플팩_데이터구조_설명.md)** | nodes.jsonl, edges.jsonl 등 각 파일의 형식과 역할 설명 | 데이터 파일이 **왜 이렇게 생겼나** 궁금할 때 |

---

### 🐍 Python 스크립트 — 실행 가능한 실습 도구

| 파일 | 목적 | 선행 설치 |
|------|------|----------|
| **[explore.py](explore.py)** | 온톨로지 구조 탐색 (통계·관계·검색·Claim추적) | 없음 — 바로 실행 가능 |
| **[import_to_neo4j.py](import_to_neo4j.py)** | Neo4j에 노드/엣지 데이터 자동 적재 | `pip install neo4j` + Neo4j 실행 |
| **[ai_context.py](ai_context.py)** | 그래프 → AI 컨텍스트 변환 (오프라인/API 모드) | 오프라인은 없음 / API는 anthropic |

---

### 📊 데이터 파일 — 온톨로지 샘플 (프로그래밍 언어 생태계)

```
sample_pack/
├── graph/
│   ├── nodes.jsonl   ← 노드 34개 (9 시맨틱 스페이스 전부 포함)
│   └── edges.jsonl   ← 엣지 48개 (12가지 관계 타입)
└── cloud/
    ├── documents.jsonl  ← 원본 문서 5개
    └── chunks.jsonl     ← 문장 단위 청크 24개
```

### 📦 기타

| 파일 | 목적 |
|------|------|
| `programming_lang_pack.zip` | OpenCrab 업로드용 ZIP (cloud/ + graph/ 패키징) |
| `queries.cypher` | Neo4j Browser에서 실행하는 Cypher 쿼리 모음 (LEVEL 1~7) |

---

## 🚀 빠른 시작 (지금 당장 할 수 있는 것)

```powershell
# 1. 저장소 클론
git clone https://github.com/kEEPpp/ontology_study.git
cd ontology_study

# 2. 온톨로지 구조 탐색 (설치 없이 바로)
python explore.py

# 3. AI 컨텍스트 생성 (설치 없이 바로)
python ai_context.py
# → 1 선택 → 질문 입력 → generated_context.txt 생성
# → 이 파일을 claude.ai에 붙여넣으면 온톨로지 기반 답변
```

---

## 📚 권장 학습 순서

```
1️⃣  01_개념학습 읽기          → "온톨로지가 뭔지" 이해
        ↓
2️⃣  02_실습흐름도 확인         → "뭘 어떤 순서로 해야 하나" 파악
        ↓
3️⃣  python explore.py        → 샘플 데이터 직접 탐색
        ↓
4️⃣  sample_pack 데이터 구조    → nodes.jsonl 파일 직접 열어서 읽기
        ↓
5️⃣  Neo4j 설치               → import_to_neo4j.py → queries.cypher
        ↓
6️⃣  python ai_context.py     → 온톨로지를 AI 지식으로 주입
        ↓
7️⃣  커스텀 온톨로지 설계       → 내 도메인으로 nodes.jsonl 직접 작성
```

---

*학습 기반: OpenCrab 베타테스터 카카오톡 그룹 대화 (485명, 2026-05-20~27)*
