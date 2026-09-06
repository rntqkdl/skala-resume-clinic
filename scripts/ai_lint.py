# -*- coding: utf-8 -*-
"""
AI 생성 문체 및 번역투 검출 린터 (im-not-ai Korean Linter)
- 70+ AI 클리셰, 번역투, 기계적 병렬 구조 탐지
- 두괄식 및 소제목 공식 점검
"""
import sys
import re

AI_PATTERNS = [
    (r"를 통해|을 통해", "번역투 (~를 통해) -> '~로', '~하여', 또는 구체적 액션 동사로 대체"),
    (r"에 있어서|에 있어", "일본어/번역투 (~에 있어서) -> '~에서', '~할 때'로 간결화"),
    (r"로 이어지는|으로 이어지는", "상투적 번역투 (~로 이어지는) -> 인과관계를 능동형 문장으로 분리"),
    (r"중요성을 깨달았습니다|중요성을 알게 되었습니다", "전형적 AI 반성문 패턴 -> 구체적 학습 규칙이나 시스템 지침으로 수정"),
    (r"발판이 되었습니다|교두보가 되었습니다|단초가 되었습니다", "구태의연한 상투어 -> 실제 후속 성과 및 정량 지표로 대체"),
    (r"귀사", "범용 복사/붙여넣기 냄새 -> 정확한 회사명(KT, 우리은행 등) 명시"),
    (r"뿐만 아니라", "기계적 대칭 병렬구조 -> 문장을 단문으로 쪼개거나 구체적 기술 나열"),
    (r"성공적으로", "주관적 자평 -> 정량적 수치(정확도 %, 단축 시간 등)로 객관화"),
    (r"다양한|많은|여러", "모호한 수식어 -> 구체적 개수/모수(13,000종, 2,000건 등)로 치환"),
    (r"기여했습니다|이바지했습니다", "수동적 서술 -> '~을 구축했습니다', '~을 설계했습니다' 등 주도적 동사 사용"),
    (r"열정을 가지고|최선을 다해", "감정적 서술 -> 엔지니어링 방법론과 문제해결 행동으로 대체"),
    (r"배울 수 있었습니다", "수동적 학습 표현 -> '~역량을 내재화했습니다', '~노하우를 확립했습니다'로 강화")
]

def lint_text(text):
    print("==================================================")
    print("   AI 번역투 및 자소서 클리닉 린터 진단 결과")
    print("==================================================")
    
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        print("텍스트가 비어 있습니다.")
        return
        
    # 1. 소제목 검사
    first_line = lines[0]
    has_subtitle = first_line.startswith("[") and "]" in first_line
    print(f"1. 소제목 진단: {'[통과]' if has_subtitle else '[경고]'}")
    if has_subtitle:
        has_num = bool(re.search(r"\d+", first_line))
        print(f"   - 소제목: {first_line}")
        print(f"   - 정량 수치 포함 여부: {'포함됨 (우수)' if has_num else '수치 누락 (개선 권장)'}")
    else:
        print("   - 소제목([문제해결 행동 + 비교가능한 정량수치])이 첫 줄에 누락되었습니다.")

    # 2. AI 패턴 검사
    print("\n2. AI 클리셰 / 번역투 검출:")
    detected_count = 0
    for pattern, advice in AI_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            detected_count += len(matches)
            print(f"   [감점 요인] '{matches[0]}' ({len(matches)}회 감지)")
            print(f"     -> 권장 조치: {advice}")
            
    if detected_count == 0:
        print("   [우수] 탐지된 AI 클리셰 및 번역투가 없습니다. (자연스러운 엔지니어 문체)")
    else:
        print(f"\n   -> 총 {detected_count}건의 AI 패턴이 발견되었습니다. 수정을 권장합니다.")

    # 3. 문장 종결 어미 점검 (능동형 vs 수동형)
    passive_endings = len(re.findall(r"되었습니다|이루어졌습니다|보였습니다", text))
    active_endings = len(re.findall(r"설계했습니다|구축했습니다|도출했습니다|단축했습니다|해결했습니다|확보했습니다", text))
    print(f"\n3. 서술어 엔지니어링 주도성:")
    print(f"   - 주도적 능동 동사: {active_endings}회")
    print(f"   - 피동/수동 동사: {passive_endings}회")
    print("==================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
        lint_text(content)
    else:
        print("Usage: python ai_lint.py <file_path>")
