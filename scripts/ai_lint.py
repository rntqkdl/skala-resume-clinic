# -*- coding: utf-8 -*-
"""
AI 생성 문체 및 번역투 검출 린터 (im-not-ai Powered Tech Resume Linter)
- epoko77-ai/im-not-ai 10대 카테고리 기반 70개 서브 패턴 정밀 탐지
- S1(치명적 감점), S2(경고) 심각도 분류 및 HEI(인간 엔지니어링 지수) 산출
- 두괄식, 소제목 정량 수치, 능동형 서술어 비율 종합 진단
"""
import sys
import os
import re
import json

DEFAULT_DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "ai_ban_dictionary.json")

def load_rules(dict_path=DEFAULT_DICT_PATH):
    if os.path.exists(dict_path):
        try:
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("rules", []), data.get("categories", {})
        except Exception as e:
            print(f"[경고] 사전 파일 로드 실패: {e}")
    return [], {}

def lint_text(text, rules=None, categories=None):
    if rules is None:
        rules, categories = load_rules()
        
    print("=" * 65)
    print("   im-not-ai 기반 공채 자기소개서 정밀 린터 진단 결과")
    print("=" * 65)
    
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        print("텍스트가 비어 있습니다.")
        return 0
        
    # 1. 소제목 진단
    first_subtitle_line = ""
    for line in lines:
        cleaned = line.lstrip("#").strip()
        if cleaned.startswith("[") and "]" in cleaned:
            first_subtitle_line = cleaned
            break
        
    has_subtitle = bool(first_subtitle_line)
    has_num_in_sub = bool(re.search(r"\d+", first_subtitle_line)) if has_subtitle else False
    
    print("\n1. 소제목 공식 검증:")
    if has_subtitle:
        print(f"   - 소제목: {first_subtitle_line}")
        print(f"   - 정량 수치/모수 포함: {'[PASS] 포함됨' if has_num_in_sub else '[FAIL] 수치 누락 (모수 추가 필요)'}")
    else:
        print("   - [FAIL] 소제목([문제해결 행동 + 비교가능한 정량수치]) 누락")

    # 2. im-not-ai 패턴 검사
    print("\n2. AI 클리셰 및 번역투 검출 (im-not-ai 10대 카테고리):")
    s1_violations = []
    s2_violations = []
    
    for rule in rules:
        rule_id = rule.get("id", "N/A")
        cat = rule.get("category", "A")
        cat_name = categories.get(cat, cat)
        severity = rule.get("severity", "S2")
        pattern_regex = rule.get("regex", "")
        reason = rule.get("reason", "")
        replacement = rule.get("replacement", "")
        
        if not pattern_regex:
            continue
            
        matches = list(re.finditer(pattern_regex, text))
        if matches:
            violation_info = {
                "id": rule_id,
                "category": cat_name,
                "severity": severity,
                "count": len(matches),
                "sample": matches[0].group(),
                "reason": reason,
                "replacement": replacement
            }
            if severity == "S1":
                s1_violations.append(violation_info)
            else:
                s2_violations.append(violation_info)
                
    total_violations = len(s1_violations) + len(s2_violations)
    if total_violations == 0:
        print("   [우수] 탐지된 AI 클리셰 및 번역투 0건 (완벽한 엔지니어링 문체)")
    else:
        if s1_violations:
            print(f"   * S1 치명적 AI 클리셰 ({len(s1_violations)}건 감지 - 즉시 탈락 요인):")
            for v in s1_violations:
                print(f"     - [{v['id']}] '{v['sample']}' ({v['count']}회) -> {v['reason']}")
                print(f"       -> 권장 조치: {v['replacement']}")
        if s2_violations:
            print(f"   * S2 번역투/문체 완곡 ({len(s2_violations)}건 감지):")
            for v in s2_violations:
                print(f"     - [{v['id']}] '{v['sample']}' ({v['count']}회) -> {v['reason']}")
                print(f"       -> 권장 조치: {v['replacement']}")

    # 3. 서술어 능동성 분석
    passive_endings = len(re.findall(r"되었습니다|이루어졌습니다|보여집니다|생각됩니다|판단됩니다", text))
    active_endings = len(re.findall(r"설계했습니다|구축했습니다|도출했습니다|단축했습니다|해결했습니다|최적화했습니다|입증했습니다|달성했습니다|구현했습니다|적용했습니다", text))
    total_verbs = active_endings + passive_endings
    active_ratio = (active_endings / total_verbs * 100) if total_verbs > 0 else 0
    
    print("\n3. 서술어 엔지니어링 주도성:")
    print(f"   - 능동형 주도 동사: {active_endings}회")
    print(f"   - 피동/수동형 동사: {passive_endings}회")
    print(f"   - 능동 서술어 비율: {active_ratio:.1f}% ({'[PASS] 70% 이상' if active_ratio >= 70 else '[FAIL] 능동 전환 필요'})")

    # 4. 종합 HEI (Human Engineering Index) 산출
    score = 100
    score -= len(s1_violations) * 15
    score -= len(s2_violations) * 5
    if not has_subtitle or not has_num_in_sub:
        score -= 10
    if active_ratio < 60:
        score -= 10
    score = max(0, min(100, score))
    
    print("\n" + "-" * 65)
    print(f"   종합 판정: HEI(인간 엔지니어링 지수) = {score} / 100점")
    if score >= 90:
        print("   [합격권] 서류 통과 가능성 최우수 (AI 티 제로 및 능동 엔지니어링)")
    elif score >= 75:
        print("   [보통] 경미한 번역투 및 서술어 정제 필요")
    else:
        print("   [위험] S1 클리셰 다수 검출 또는 수동형 서술 과다 (재작성 권장)")
    print("=" * 65)
    return score

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"[오류] 파일을 찾을 수 없습니다: {file_path}")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        lint_text(content)
    else:
        print("Usage: python scripts/ai_lint.py <file_path>")

