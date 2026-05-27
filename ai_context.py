"""
온톨로지 → AI 컨텍스트 변환 스크립트
- OpenCrab 없이 그래프 데이터를 AI(Claude/GPT)의 컨텍스트로 직접 주입
- Neo4j 없어도 동작 (JSONL 파일 직접 사용)
- 실행: python ai_context.py

두 가지 모드:
  1. 오프라인 모드: 그래프를 텍스트로 변환해서 콘솔 출력 (Claude에 붙여넣기)
  2. API 모드:      Anthropic SDK로 직접 질의 (pip install anthropic 필요)
"""

import json, sys, io
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = Path(__file__).parent / "sample_pack"


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ══════════════════════════════════════════════════════════════
# 핵심: 그래프 → 자연어 컨텍스트 변환
# AI가 구조화된 지식을 이해할 수 있는 텍스트로 변환하는 로직
# ══════════════════════════════════════════════════════════════

def graph_to_context(question: str = "", space_filter: str = "") -> str:
    """
    그래프 데이터를 AI에게 줄 컨텍스트 문자열로 변환.

    space_filter: 특정 시맨틱 스페이스만 포함 (예: "Subject,Claim,Evidence")
                  비어있으면 전체 포함
    """
    nodes = load_jsonl(BASE / "graph/nodes.jsonl")
    edges = load_jsonl(BASE / "graph/edges.jsonl")
    node_map = {n["id"]: n for n in nodes}

    # 질문과 관련된 노드만 필터링 (키워드 기반 간단 필터)
    if question:
        keywords = question.lower().split()
        def is_relevant(node):
            text = (node["label"] + " " +
                    str(node.get("properties", {}))).lower()
            return any(kw in text for kw in keywords)
        relevant_ids = {n["id"] for n in nodes if is_relevant(n)}
        # 관련 노드의 이웃도 포함 (1-hop)
        for edge in edges:
            if edge["source"] in relevant_ids:
                relevant_ids.add(edge["target"])
            if edge["target"] in relevant_ids:
                relevant_ids.add(edge["source"])
        filtered_nodes = [n for n in nodes if n["id"] in relevant_ids]
        filtered_edges = [e for e in edges
                          if e["source"] in relevant_ids and e["target"] in relevant_ids]
    else:
        filtered_nodes = nodes
        filtered_edges = edges

    # 스페이스 필터
    if space_filter:
        spaces = [s.strip() for s in space_filter.split(",")]
        filtered_nodes = [n for n in filtered_nodes if n.get("space") in spaces]
        valid_ids = {n["id"] for n in filtered_nodes}
        filtered_edges = [e for e in filtered_edges
                          if e["source"] in valid_ids and e["target"] in valid_ids]

    # ── 컨텍스트 문자열 구성 ──
    lines = []
    lines.append("=== 온톨로지 지식 그래프 ===")
    lines.append(f"(노드 {len(filtered_nodes)}개, 관계 {len(filtered_edges)}개)\n")

    # 시맨틱 스페이스별로 그룹화해서 출력
    space_groups = defaultdict(list)
    for n in filtered_nodes:
        space_groups[n.get("space", "기타")].append(n)

    space_descriptions = {
        "Subject":   "주체 (행위자/핵심 개체)",
        "Resource":  "리소스 (도구/프레임워크/라이브러리)",
        "Evidence":  "증거 (출처/근거 데이터)",
        "Concept":   "개념 (추상적 지식/패러다임)",
        "Result":    "결과 (측정된 아웃풋)",
        "Claim":     "클레임 (주장/판단)",
        "Community": "커뮤니티 (생태계/조직)",
        "Policy":    "정책 (규칙/표준)",
        "Intensity": "강도 (친화도/점수)",
    }

    for space, desc in space_descriptions.items():
        group = space_groups.get(space, [])
        if not group:
            continue
        lines.append(f"[{space}: {desc}]")
        for n in group:
            props = n.get("properties", {})
            prop_str = ""
            if "description" in props:
                prop_str = f" — {props['description'][:80]}"
            elif "confidence" in props:
                prop_str = f" — 신뢰도: {props['confidence']}"
            elif "score" in props:
                prop_str = f" — 점수: {props['score']}"
            lines.append(f"  • {n['label']}{prop_str}")
        lines.append("")

    # 관계 출력
    lines.append("[관계 목록]")
    rel_groups = defaultdict(list)
    for e in filtered_edges:
        rel_groups[e["relation"]].append(e)

    for rel, rel_edges in sorted(rel_groups.items()):
        lines.append(f"  {rel}:")
        for e in rel_edges:
            src = node_map.get(e["source"], {}).get("label", e["source"])
            tgt = node_map.get(e["target"], {}).get("label", e["target"])
            strength = e.get("properties", {}).get("strength", "")
            strength_str = f" (강도: {strength})" if strength else ""
            lines.append(f"    {src} → {tgt}{strength_str}")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# 모드 1: 오프라인 — 컨텍스트 텍스트 출력 (Claude에 직접 붙여넣기)
# ══════════════════════════════════════════════════════════════

def offline_mode():
    print("\n[오프라인 모드] 질문을 입력하면 관련 그래프 컨텍스트를 생성합니다.")
    print("이 텍스트를 Claude나 GPT 채팅창에 붙여넣어 사용하세요.\n")

    question = input("질문 (비우면 전체 그래프): ").strip()
    context = graph_to_context(question)

    print("\n" + "="*60)
    print("아래 텍스트를 복사해서 AI에게 붙여넣으세요:")
    print("="*60 + "\n")

    system_prompt = f"""당신은 아래 온톨로지 지식 그래프를 기반으로 질문에 답합니다.
그래프의 노드(개념)와 엣지(관계)를 활용해서 구조화된 답변을 주세요.
근거가 되는 Evidence 노드가 있다면 반드시 언급하세요.

{context}
---
질문: {question if question else '이 온톨로지에 대해 전반적으로 설명해주세요.'}"""

    print(system_prompt)
    print("\n" + "="*60)

    # 파일로도 저장
    out_path = Path(__file__).parent / "generated_context.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(system_prompt)
    print(f"\n[저장됨] {out_path}")


# ══════════════════════════════════════════════════════════════
# 모드 2: API 모드 — Anthropic SDK 직접 호출
# ══════════════════════════════════════════════════════════════

def api_mode():
    try:
        import anthropic
    except ImportError:
        print("\n[오류] anthropic 패키지가 없습니다.")
        print("  설치: pip install anthropic")
        return

    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("\n[오류] ANTHROPIC_API_KEY 환경변수가 없습니다.")
        print("  설정: $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
        return

    print("\n[API 모드] Claude에게 직접 질의합니다.")
    question = input("질문: ").strip()
    if not question:
        print("질문을 입력해주세요.")
        return

    context = graph_to_context(question)

    print("\nClaude에게 질의 중...\n")
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=f"""당신은 아래 온톨로지 지식 그래프를 기반으로 질문에 답합니다.
그래프의 노드(개념)와 엣지(관계)를 활용해서 구조화된 답변을 주세요.
근거가 되는 Evidence 노드가 있다면 반드시 언급하세요.

{context}""",
        messages=[{"role": "user", "content": question}],
    )

    print("─" * 50)
    print(message.content[0].text)
    print("─" * 50)
    print(f"\n[사용 토큰] 입력: {message.usage.input_tokens} / 출력: {message.usage.output_tokens}")


# ══════════════════════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🤖 온톨로지 → AI 컨텍스트 변환기")
    print("  이 도구는 OpenCrab 없이 그래프 데이터를 AI에게 직접 주입합니다.\n")
    print("  1. 오프라인 모드 — 컨텍스트 텍스트 생성 (붙여넣기용)")
    print("  2. API 모드      — Claude에게 직접 질의 (ANTHROPIC_API_KEY 필요)")

    choice = input("\n선택 (1/2): ").strip()
    if choice == "1":
        offline_mode()
    elif choice == "2":
        api_mode()
    else:
        print("잘못된 입력")
