# 📖 01. 온톨로지 개념 학습 가이드
### — OpenCrab 베타테스터 카카오톡 대화(485명) 분석 기반 —
### 대상: 온톨로지가 무엇인지, 어떤 용어를 쓰는지 처음 공부하는 단계

> 출처: OpenCrab 베타테스터 카카오톡 그룹 대화 (2026-05-20 ~ 2026-05-27)  
> 이 문서의 목적: **개념 이해** (도구 사용법 X, 실습 방법 X)

---

## 📚 1. Ontology 공부 Step

### Step 1 — 개념 이해: "온톨로지란 무엇인가?"

온톨로지는 **지식을 구조화된 그래프(개념-관계-증거)로 표현하는 방식**입니다.  
일반 RAG/GraphRAG와의 차이점은 명확한 **도메인 지향성**(의도·정책·문법)을 가진다는 것입니다.

> 💬 대화 중 핵심 설명:
> - "데이터를 개념, 의미, 관계성 그래프로 잘 정의하면 그게 온톨로지고 저장방식이 그래프DB다"
> - "온톨로지는 도메인 지향적 / 문법의 존재 / 활용 목표의 존재 / 권한 적용 가능이라는 특징을 가짐"
> - "사람 자체가 온톨로지. AI가 보기 쉽게 만들어서 주머니에 넣고 다니는 형태"

**9가지 시맨틱 스페이스 (OpenCrab의 문법)**

| # | 스페이스 | 역할 |
|---|---------|------|
| 1 | 주체 (Subject) | 행위자/개체 |
| 2 | 리소스 (Resource) | 데이터/자원 |
| 3 | 증거 (Evidence) | 근거/출처 |
| 4 | 개념 (Concept) | 추상적 지식 |
| 5 | 결과 (Result) | 아웃풋 |
| 6 | 클레임 (Claim) | 주장/판단 |
| 7 | 커뮤니티 (Community) | 관계/그룹 |
| 8 | 정책 (Policy) | 규칙/기준 |
| 9 | 강도 (Intensity) | 중요도/가중치 |

---

### Step 2 — 핵심 용어 숙지

**AI 에이전트 핵심 용어 (대화에서 언급된 항목)**

| 용어 | 설명 |
|------|------|
| **RAG** | 검색 증강 생성 (실무에서 "레그"로 발음 통일 권고) |
| **GraphRAG** | 그래프 기반 RAG (온톨로지와 유사하나 문법/의도 없음) |
| **MCP** | Model Context Protocol — AI 툴 연결 표준 프로토콜 |
| **온톨로지** | 도메인 지향적 구조화 지식 체계 |
| **지식 그래프** | 개념 간 관계를 그래프로 표현한 구조 |
| **인제스트** | 데이터를 온톨로지/팩으로 변환하는 과정 |
| **역방향 인제스트** | AI와의 대화 결과를 다시 온톨로지에 저장하는 선순환 |
| **노드/엣지** | 그래프의 구성 요소 (노드=개념, 엣지=관계) |
| **청크 (Chunk)** | 데이터를 적절한 크기로 쪼갠 단위 (문장 단위 권장) |
| **Evidence** | 각 노드/클레임에 연결된 출처/근거 |
| **벡터 DB** | 임베딩 기반 유사도 검색 데이터베이스 |
| **Semantic/Kinetic** | 의미적(정적) / 운동학적(동적) 온톨로지 구분 |
| **Neo4j** | 그래프 DB — 로컬에서 팩 빌딩 시 사용 (무료) |

---

### Step 3 — 구조 이해: RAG vs 온톨로지 vs GraphRAG 비교

| 구분 | RAG | GraphRAG | 온톨로지 (OpenCrab) |
|------|-----|----------|---------------------|
| 데이터 관리 | 범용적 | 범용적 | **도메인 지향적** |
| 문법 | 없음 | 없음 | **있음 (9문법)** |
| 활용 목표 | 불분명 | 불분명 | **명확** |
| 깊이 적용 | 불가 | 부분 가능 | **가능** |
| 의도/컨셉 | 없음 | 없음 | **있음** |
| 재사용성 | 낮음 | 낮음 | **높음** |

---

### Step 4 — 팩(Pack) 개념 습득

- **온톨로지 팩** = 특정 도메인 지식을 구조화한 최소 단위
- 팩은 **하나의 역할/범위**를 명확히 정의해야 함
- 여러 팩을 **프로젝트로 묶어** 관련 지식을 연결
- 팩의 품질 기준: 노드 수, 엣지 수, Evidence 완성도, QA 통과율

> 💬 핵심 조언:  
> "일단 작게 하나 만들어서 똑바로 돌아가는지 점검해 보고, 잘 돌아가는걸 확인 후 확장해라" — 99%가 동의한 피드백

---

### Step 5 — 실전: 팩 수집 → 확장 → QA → MVP 완성

```
1차 수집 → 2차 확장 → 3차 QA → MVP 배포 → 사용하며 보강
```

- **QA 툴**: LocalCrab 내장 (목표치 100% 수렴 확인)
- **완료 기준**: 사용자가 직접 지정 (AI는 목표 없이 무한 확장할 수 있음)
- **Evidence 레버**: 디테일이 중요한 팩일수록 Evidence를 꼼꼼히 챙길 것

---

## 🔧 2. Ontology 구축 및 실습 절차

### 🚀 전체 워크플로우

```
[1단계] 목적/도메인 정의
         ↓
[2단계] 데이터 수집 (로컬크랩 or 코덱스/GPT 활용)
         ↓
[3단계] 온톨로지 빌딩 (LocalCrab + Neo4j)
         ↓
[4단계] ZIP 패키징 및 인제스트
         ↓
[5단계] OpenCrab에 팩 업로드
         ↓
[6단계] MCP URL 생성 → AI 도구와 연결
         ↓
[7단계] QA 테스트 및 보강 (역방향 인제스트)
         ↓
[8단계] (선택) 웹앱/서비스로 확장
```

---

### 📋 단계별 상세 가이드

#### 1단계 — 목적 및 도메인 정의

팩을 만들기 전에 반드시 결정해야 할 것들:

- **주제 범위**: 너무 넓지 않게, 한 팩 = 한 역할
- **대상 사용자**: 본인 업무용? 공개용? B2B?
- **활용 목표**: AI에게 무엇을 물어볼 것인가?
- **데이터 출처**: 어떤 데이터를 어디서 가져올 것인가?

> 💡 팁: 여러 팩을 묶을 때는 분야별로 쪼개서 각자 역할을 명확히 한 뒤 프로젝트로 묶어라

**팩 분류 예시 (건물 관리 케이스)**
```
건물_공사팩 / 건물_보수팩 / 인적사항팩 / 클라이언트팩 / 규제팩
→ 하나의 프로젝트로 묶어 운용
```

---

#### 2단계 — 데이터 수집

| 방법 | 도구 | 특징 |
|------|------|------|
| 직접 크롤링 | Codex, Claude Code | 자동화, 대용량 수집 가능 |
| 파일 업로드 | PDF, MD, TXT 등 | 기존 보유 자료 활용 |
| URL 인제스트 | OpenCrab 웹 UI | 페이지 내 페이지는 미지원 |
| GitHub URL | OpenCrab 웹 UI | 대용량에 적합 |
| 카카오톡 대화 내보내기 | 수동 추출 후 정제 | 암묵지 수집에 효과적 |

> ⚠️ 주의: 대화방 데이터는 농담/주제 이탈 내용 필터링 필수

---

#### 3단계 — 온톨로지 빌딩 (LocalCrab)

**LocalCrab 설치**
- GitHub: [AlexAI-MCP/OpenCrab](https://github.com/AlexAI-MCP/OpenCrab)
- 설치 보조 도구: [Opencrab_installer](https://github.com/contentscoin/Opencrab_installer.git)

**빌딩 프롬프트 예시 (Claude Code / Codex 사용 시)**
```
1. LocalCrab MCP로 설치하고 세팅해
2. [주제] 관련 자료를 500개 이상의 노드로 구성하고 
   Neo4j로 그래프 사이퍼까지 해서 zip 파일로 만들어줘
```

**청크 기준**
- ✅ 문장 단위 (권장)
- ❌ 단어 단위 (너무 잘게 → 품질 저하)
- ❌ 쉼표 단위 (과잉 분할)

**Data ZIP 인제스트 기준 (공식)**
```
필수 구조:
- Cloud Pack: cloud/documents.jsonl, cloud/chunks.jsonl,
              graph/nodes.jsonl, graph/edges.jsonl
- Graph Pack: graph/nodes.jsonl + edges.jsonl (또는 ontology/ 폴더)

허용 확장자: .md .txt .csv .tsv .json .jsonl .yaml .yml .xml .html .htm .pdf

제한:
- 단일 파일 5MB 이하 (완화 가능: 최대 20~30MB)
- ZIP 파일 엔트리 최대 500개
- Graph node: id 필수
- Graph edge: source/target 또는 from/to 필수
```

---

#### 4단계 — OpenCrab 등록 및 인제스트

**접속 및 가입**: [https://opencrab.sh/](https://opencrab.sh/)

```
1. 이메일 인증 또는 Google Auth 가입
2. 로그인 후 마켓플레이스 이동
3. Ingest 탭에서 Data ZIP 업로드
4. 인제스트 히스토리에서 "Create Pack" 클릭
5. 팩 이름 설정 (Private/Public 선택)
6. "Save Pack" 저장
```

**서비스 티어별 권한**

| 티어 | 팩 생성 | 역방향 인제스트 | 프로젝트 | 워크플로우 | 팩 판매 |
|------|---------|----------------|----------|-----------|---------|
| Free | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pro | ✅ | ❌ | 2개 | ❌ | ❌ |
| Expert | ✅ | ✅ (양방향) | 무제한 | ✅ | ✅ |

---

#### 5단계 — MCP 연결 및 AI 도구 사용

```
대시보드 → MCP 탭 (우측 상단) → URL 복사
→ GPT, Claude, Codex, Claude Code, Cursor 등에 Remote MCP로 등록
```

**연결 후 사용 예시**
```
"[팩이름] 팩을 로드하고 [질문]을 해줘"
"이 팩에서 [개념]과 [개념]의 관계를 분석해줘"
"팩 리스트업 해줘" (설치된 팩 확인)
```

---

#### 6단계 — QA 및 역방향 인제스트 (Expert 기능)

**QA 테스트**
- LocalCrab 내장 QA 툴로 목표치 100% 수렴 여부 확인
- 자주 묻는 질문 미리 만들어 테스트

**역방향 인제스트** (Expert 전용)
- AI와의 대화 결과 → 다시 온톨로지로 저장
- "시멘틱한 방식으로 지식을 누적"하는 핵심 기능
- 노션·옵시디언 없이도 회의록·아이디어 관리 가능

```
예시: GPT와 회의 → 결과를 역방향 인제스트 → 팩에 자동 반영
```

---

#### 7단계 — 웹앱/서비스로 확장 (선택)

팩을 백엔드로 활용한 서비스 제작 예시:
- GitHub Pages로 온톨로지 시각화 대시보드
- Vercel + OpenCrab API 연동 웹앱
- GPT 이미지 생성 → PDF로 묶어 발표자료 제작

> 참고 예시: [헬스케어 온톨로지 대시보드](https://tteggu87.github.io/demo-healthcare-ontology/)

---

## 🔗 3. 공부에 도움이 되는 링크 정리

### 🦀 OpenCrab 관련

| 링크 | 설명 |
|------|------|
| [https://opencrab.sh/](https://opencrab.sh/) | OpenCrab 메인 서비스 — 온톨로지 팩 마켓플레이스 |
| [https://opencrab.sh/pet/snu](https://opencrab.sh/pet/snu) | OpenCrab 서울대 합격 전략 페이지 (데모 케이스) |
| [https://forms.gle/JGKGSyj5F2ngD1Um7](https://forms.gle/JGKGSyj5F2ngD1Um7) | 베타 설문 (PRO 티어 무료 제공) |

---

### 📦 GitHub — 도구 및 설치

| 링크 | 설명 |
|------|------|
| [https://github.com/AlexAI-MCP/OpenCrab](https://github.com/AlexAI-MCP/OpenCrab) | LocalCrab (로컬크랩) 공식 GitHub — MCP 서버 설치 및 세팅 |
| [https://github.com/contentscoin/Opencrab_installer.git](https://github.com/contentscoin/Opencrab_installer.git) | OpenCrab 설치 보조 도구 (에펨쥐님 제작) |
| [https://github.com/chrisryugj/korean-stats-mcp](https://github.com/chrisryugj/korean-stats-mcp) | 한국 통계청 MCP — 팩 제작 시 통계 데이터 활용 |
| [https://github.com/etehofk1-ops/opencrab-guide-map](https://github.com/etehofk1-ops/opencrab-guide-map) | OpenCrab 가이드 맵 GitHub (에테호님 제작) |
| [https://github.com/Q00/ouroboros](https://github.com/Q00/ouroboros) | Ouroboros — 자동화 관련 GitHub |
| [https://github.com/trykimu/videoeditor](https://github.com/trykimu/videoeditor) | 영상 편집 자동화 도구 GitHub |
| [https://github.com/zjunlp/SciAtlas](https://github.com/zjunlp/SciAtlas) | 과학 지식 아틀라스 — 온톨로지 데이터 참고용 |
| [https://gitlab.com/fabriciotelles/skills](https://gitlab.com/fabriciotelles/skills) | 스킬/하네스 관련 GitLab |

---

### 🎥 YouTube — 학습 영상

| 링크 | 설명 |
|------|------|
| [https://youtu.be/hRpSg3i-_Rg](https://youtu.be/hRpSg3i-_Rg) | Alexai 유튜브 — LocalCrab 사용법 (후반부에 상세 설명) |
| [https://youtu.be/6fD5pi6WcfM](https://youtu.be/6fD5pi6WcfM) | 이현종 대표 유튜브 — 온톨로지 용어 설명 영상 |
| [https://youtu.be/KsGF34fcLXc](https://youtu.be/KsGF34fcLXc) | OpenCrab MCP 연결 방법 영상 |

---

### 🌐 웹사이트 — 데모 및 도구

| 링크 | 설명 |
|------|------|
| [https://tteggu87.github.io/demo-healthcare-ontology/](https://tteggu87.github.io/demo-healthcare-ontology/) | 헬스케어 온톨로지 대시보드 (GitHub Pages 데모, 읽기쓰기님 제작) |
| [https://opencrab-guide-map.vercel.app/](https://opencrab-guide-map.vercel.app/) | OpenCrab 가이드 맵 (에테호님 제작 — 깔끔한 UI 가이드) |
| [https://https-opencrab-sh-api-mcp-ocm.vercel.app/](https://https-opencrab-sh-api-mcp-ocm.vercel.app/) | Pack Builder 웹앱 (에펨쥐님 제작) |
| [https://crab-guide.pages.dev/](https://crab-guide.pages.dev/) | OpenCrab 가이드 사이트 |
| [https://amazingsyp.github.io/pokemon-ontology/](https://amazingsyp.github.io/pokemon-ontology/) | 포켓몬 온톨로지 (학습용 예시) |
| [https://www.muton.co.kr/](https://www.muton.co.kr/) | 사유ing님 브랜드 포트폴리오 사이트 (AI로 제작한 사례) |
| [https://bigster.co.kr/](https://bigster.co.kr/) | 빅스터 (이현종 대표, 온톨로지 책 저자) |

---

### 📖 블로그 & 아티클

| 링크 | 설명 |
|------|------|
| [https://blog.naver.com/oppamarketing/224292425915](https://blog.naver.com/oppamarketing/224292425915) | 온톨로지 기반 자동화 글쓰기 1탄 (에펨쥐님) |
| [https://blog.naver.com/oppamarketing/224293086504](https://blog.naver.com/oppamarketing/224293086504) | 온톨로지 기반 자동화 글쓰기 2탄 |
| [https://m.blog.naver.com/steavenjobs/224296062740](https://m.blog.naver.com/steavenjobs/224296062740) | OpenCrab 관련 블로그 |
| [https://blog.naver.com/steavenjobs/224294235632](https://blog.naver.com/steavenjobs/224294235632) | OpenCrab 실습 후기 블로그 |

---

### 🛠️ 기타 도구 & 참고 자료

| 링크 | 설명 |
|------|------|
| [https://joonan30.github.io/slack-ai-assistant-guide/](https://joonan30.github.io/slack-ai-assistant-guide/) | Slack AI 어시스턴트 가이드 — 안준용 교수, 학술 자동화 활용법 |
| [https://notebooklm.google.com/...](https://notebooklm.google.com/notebook/624497ff-c8d9-48a3-bef7-176dd5f32655/artifact/67c21d95-6f8b-442f-817b-2d784ae168e8) | Google NotebookLM — 온톨로지 학습 자료 (아티팩트 공유) |
| [https://arxiv.org/pdf/2603.17244](https://arxiv.org/pdf/2603.17244) | 온톨로지/AI 관련 arXiv 논문 |
| [https://www.kcsc.re.kr/](https://www.kcsc.re.kr/) | 방송통신심의위원회 공식 사이트 (공공 데이터 수집 참고) |
| [https://suno.com/s/1MCSZpdKXq6X5aHs](https://suno.com/s/1MCSZpdKXq6X5aHs) | Suno AI 음악 생성 (온톨로지 활용 창작 사례) |
| [https://www.gpters.org/law/post/based-survey-automation-customized-QACVckjAkCzxP8R](https://www.gpters.org/law/post/based-survey-automation-customized-QACVckjAkCzxP8R) | 법률 기반 설문 자동화 사례 |

---

## 💡 4. 핵심 인사이트 & 팁

### 🎯 팩 제작 Best Practice

1. **작게 시작하라** — 한 번에 다 하려면 100% 오류 발생
2. **팩 = 역할 1개** — 너무 일반적으로 묶지 말 것
3. **Evidence 레버를 높여라** — 디테일한 업무일수록 증거 챙기기
4. **청크는 문장 단위** — 단어/쉼표 단위로 쪼개면 품질 저하
5. **QA 먼저, 확장은 나중에** — MVP → 검증 → 개선 순서
6. **역방향 인제스트가 핵심** — AI 대화 결과를 다시 팩에 저장

### ⚠️ 주의사항

- 수집 완료 기준은 반드시 **사람이 지정** (AI는 무한 확장 시도)
- 데이터 양보다 **품질**이 중요 (6만 노드라도 의도 없으면 쓸모없음)
- 여러 팩 조합 시 **벡터 충돌** 가능 — 팩 간 역할 명확히 구분할 것
- 카카오톡/Slack 대화 데이터는 **노이즈 필터링** 필수

### 🚀 온톨로지 활용 시나리오

| 활용 사례 | 필요 팩 구성 |
|-----------|-------------|
| 개인 지식 관리 | 도메인팩 + 역방향 인제스트 |
| 제안서 자동 작성 | 기존제안서팩 + RFP팩 + 현장정보팩 |
| 이커머스 분석 | 시장조사팩 + 판매데이터팩 + CS팩 + 마진팩 |
| 건물 관리 | 공사팩 + 보수팩 + 인력팩 + 클라이언트팩 |
| 법률 문서 검토 | 법령팩 + 판례팩 + 규정팩 |
| 웹앱 서비스 | 온톨로지팩 → 백엔드 → 코덱스로 프론트 제작 |

---

## 📌 5. 온톨로지 관련 핵심 개념 요약 (웨비나 발췌)

> OpenCrab 베타테스트 웨비나 핵심 요약 (슬픈 어피치님 공유)

**"AGI 시대 생존을 위한 지식 자산화 전략"**

- 온톨로지는 **지식 자산화(Knowledge Assetization)**를 통해 의사결정 우위를 확보하는 전략
- AGI가 도래했을 때 **구조화된 지식 체계가 없다면** AI의 잠재력을 온전히 활용할 수 없음
- **9가지 시맨틱 스페이스**를 지식의 "문법"으로 삼아 데이터를 객체화
- **역방향 인제스트**로 온톨로지는 정적 데이터가 아닌 시계열적으로 진화하는 지식 체계
- 온톨로지 팩은 단순 도구를 넘어 **지식을 자산화하여 거래할 수 있는 새로운 시장** 창출

---

*문서 작성일: 2026-05-27*  
*기반 자료: OpenCrab 베타테스터 카카오톡 그룹 대화 내용*
