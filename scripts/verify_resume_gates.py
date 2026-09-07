# -*- coding: utf-8 -*-
"""
결정적 6대 하드 게이트 검증기 (Deterministic 6-Hard-Gates Validator)
- 0-LLM 결정적 코드 기반 자소서 무결성 검증
- 문항별(## 또는 문항 헤더) 자동 분할 검증 지원
- Exit Codes:
  0: ALL PASS
  1: Gate 1 FAIL (Late Conclusion)
  2: Gate 2 FAIL (Company Replaceability)
  3: Gate 3 FAIL (Missing Population / Baseline)
  4: Gate 4 FAIL (Moralistic Closing)
  5: Gate 5 FAIL (im-not-ai S1 Cliche Detected)
  6: Gate 6 FAIL (Tight Band 90~95% Length Mismatch)
"""
import sys
import os
import re
import json
import argparse

DEFAULT_DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "ai_ban_dictionary.json")

def load_s1_patterns(dict_path=DEFAULT_DICT_PATH):
    s1_regexes = []
    if os.path.exists(dict_path):
        try:
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for r in data.get("rules", []):
                    if r.get("severity") == "S1" and r.get("regex"):
                        s1_regexes.append((r["id"], r["regex"], r.get("reason", "")))
        except Exception as e:
            pass
    if not s1_regexes:
        s1_regexes = [
            ("A-1", r"(?:를|을)\s*통해", "through 직역"),
            ("C-3", r"뿐만\s*아니라", "기계적 병렬"),
            ("D-1", r"중요성을\s*(?:깨달았습니다|알게\s*되었습니다)", "반성문 패턴"),
            ("D-3", r"\b귀사\b", "범용 템플릿 의혹"),
            ("J-1", r"이바지하겠습니다|배우겠습니다", "다짐 사족")
        ]
    return s1_regexes

def verify_single_section(title, text, target_limit=800, target_company=None, min_ratio=90.0, max_ratio=95.0):
    lines = text.split("\n")
    start_idx = 0
    for idx, l in enumerate(lines):
        clean_l = l.lstrip("#").strip()
        if clean_l.startswith("[") and "]" in clean_l:
            start_idx = idx
            break
    candidate_lines = lines[start_idx:]
    clean_lines = [l.strip() for l in candidate_lines if l.strip() and not l.startswith("#")]
    pure_text = "\n".join(clean_lines)
    
    if not pure_text:
        print(f"[{title}] 텍스트가 비어 있습니다.")
        return 1
        
    char_count = len(pure_text)
    
    print("\n" + "=" * 65)
    print(f"   검증 대상: {title} (제한: {target_limit}자)")
    print("=" * 65)
    
    # Gate 1: Late Conclusion Gate
    first_150 = pure_text[:150]
    has_num_or_action = bool(re.search(r"\d+|엔지니어|역량|설계|구축|도출|달성|해결|전문가", first_150))
    is_not_passive_intro = not bool(re.search(r"어린\s*시절|호기심을\s*가지고|관심을\s*갖게", first_150))
    gate1_pass = has_num_or_action and is_not_passive_intro
    print(f"1. Gate 1 [Late Conclusion (첫 150자 두괄식 선점)]: {'[PASS]' if gate1_pass else '[FAIL]'}")
    if not gate1_pass:
        print("   -> 사유: 첫 150자 내 결론, 핵심 직무 역량 명사, 또는 대표 성과가 누락되었습니다.")

    # Gate 2: Company Replaceability Gate
    has_generic_slogan_only = bool(re.search(r"디지털\s*혁신을\s*선도|스마트\s*팩토리를\s*이끄는|AX\s*혁신", pure_text)) and not bool(re.search(r"파이프라인|트래픽|이상치|시계열|FDS|인프라|아키텍처|지연|임계값|알고리즘", pure_text))
    company_check = True
    if target_company:
        company_check = target_company in pure_text or target_company in title
    gate2_pass = (not has_generic_slogan_only) and company_check
    print(f"2. Gate 2 [Company Replaceability (도메인 락인)]: {'[PASS]' if gate2_pass else '[FAIL]'}")
    if not gate2_pass:
        if target_company and not company_check:
            print(f"   -> 사유: 지원 기업명('{target_company}')이 본문에 명시되지 않았습니다.")
        else:
            print("   -> 사유: 타사 치환 가능한 범용 슬로건이 발견되었으며 구체적 도메인 과제가 결여되었습니다.")

    # Gate 3: Missing Population Gate
    percentages = re.findall(r"(\d+(?:\.\d+)?%)", pure_text)
    gate3_pass = True
    missing_pop_details = []
    if percentages:
        for p in percentages:
            idx = pure_text.find(p)
            window = pure_text[max(0, idx-50):min(len(pure_text), idx+60)]
            has_pop = bool(re.search(r"대비|건|개|명|팀|장|종|L/h|ms|초|Baseline|F1|기존|모수|데이터셋|정확도|Top-|향상|달성|기록|오분류", window))
            if not has_pop:
                missing_pop_details.append(p)
        if missing_pop_details:
            gate3_pass = False
    print(f"3. Gate 3 [Missing Population (모수 및 베이스라인)]: {'[PASS]' if gate3_pass else '[FAIL]'}")
    if not gate3_pass:
        print(f"   -> 사유: 수치 {missing_pop_details} 주변에 비교 기준(대비/기존)이나 모수(건/개/팀/데이터셋)가 누락되었습니다.")

    # Gate 4: Moralistic Closing Gate
    tail_text = pure_text[-120:] if len(pure_text) > 120 else pure_text
    moralistic_match = re.search(r"이바지하겠습니다|배우겠습니다|성장에\s*기여하겠습니다|발전하는\s*인재가|열심히\s*하겠습니다|최선을\s*다하겠습니다", tail_text)
    gate4_pass = not bool(moralistic_match)
    print(f"4. Gate 4 [Moralistic Closing (다짐 사족 배제)]: {'[PASS]' if gate4_pass else '[FAIL]'}")
    if not gate4_pass:
        print(f"   -> 사유: 결론부 사족 감지 ('{moralistic_match.group()}'). 정량 성과 및 시스템 방어 성과로 종결하십시오.")

    # Gate 5: im-not-ai S1 Cliché Zero Gate
    s1_rules = load_s1_patterns()
    detected_s1 = []
    for r_id, regex, reason in s1_rules:
        m = re.findall(regex, pure_text)
        if m:
            detected_s1.append((r_id, m[0], len(m), reason))
    gate5_pass = len(detected_s1) == 0
    print(f"5. Gate 5 [im-not-ai S1 Cliché Zero (치명적 AI 티 0건)]: {'[PASS]' if gate5_pass else '[FAIL]'}")
    if not gate5_pass:
        print(f"   -> 사유: S1 등급 AI 클리셰 {len(detected_s1)}종 검출:")
        for r_id, sample, cnt, reason in detected_s1:
            print(f"      - [{r_id}] '{sample}' ({cnt}회): {reason}")

    # Gate 6: Tight Band Length Gate (90% ~ 95%)
    min_len = int(target_limit * (min_ratio / 100.0))
    max_len = int(target_limit * (max_ratio / 100.0))
    ratio = (char_count / target_limit) * 100 if target_limit > 0 else 0
    gate6_pass = (min_len <= char_count <= max_len)
    print(f"6. Gate 6 [Tight Band Length (공백 포함 {int(min_ratio)}%~{int(max_ratio)}%)]: {'[PASS]' if gate6_pass else '[FAIL]'}")
    print(f"   -> 글자 수: {char_count}자 / 목표: {target_limit}자 ({ratio:.1f}%) [허용 구간: {min_len}자 ~ {max_len}자]")
    if not gate6_pass:
        if char_count < min_len:
            print(f"   -> [SHORT] {min_len - char_count}자 부족: 엔지니어링 트레이드오프 및 벤치마크 조건 확장 필요")
        else:
            print(f"   -> [OVER] {char_count - max_len}자 초과: 중복 접속사, 부사, 완곡 어미 Pruning 필요")

    print("-" * 65)
    if not gate1_pass: return 1
    if not gate2_pass: return 2
    if not gate3_pass: return 3
    if not gate4_pass: return 4
    if not gate5_pass: return 5
    if not gate6_pass: return 6
    return 0

def verify_gates(content, default_limit=800, target_company=None, min_ratio=90.0, max_ratio=95.0):
    sections = re.split(r"(^## [^#\n]+)", content, flags=re.MULTILINE)
    if len(sections) > 1:
        current_title = "도입부"
        worst_code = 0
        for part in sections:
            part = part.strip()
            if not part: continue
            if part.startswith("## "):
                current_title = part.lstrip("#").strip()
            else:
                if current_title == "도입부" and len(part) < 200:
                    continue
                m = re.search(r"([\d,]+)자", current_title)
                limit = int(m.group(1).replace(",", "")) if m else default_limit
                code = verify_single_section(current_title, part, limit, target_company, min_ratio, max_ratio)
                if code != 0 and worst_code == 0:
                    worst_code = code
        return worst_code
    else:
        return verify_single_section("전체 문안", content, default_limit, target_company, min_ratio, max_ratio)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="엔터프라이즈 자소서 결정적 6대 하드 게이트 검증기")
    parser.add_argument("file", help="자소서 마크다운 파일 경로")
    parser.add_argument("limit", nargs="?", type=int, default=800, help="목표 글자 수 (기본: 800)")
    parser.add_argument("company", nargs="?", default=None, help="지원 기업명 (선택)")
    parser.add_argument("--band", choices=["tight", "standard"], default="tight", help="글자 수 허용 밴드 (tight: 90~95%, standard: 85~95%)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[오류] 파일 없음: {args.file}")
        sys.exit(99)
        
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
        
    min_r, max_r = (90.0, 95.0) if args.band == "tight" else (85.0, 95.0)
    code = verify_gates(content, args.limit, args.company, min_r, max_r)
    sys.exit(code)
