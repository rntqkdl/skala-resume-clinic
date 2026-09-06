# -*- coding: utf-8 -*-
"""
자기소개서 문항별 글자 수 정밀 계산 및 규격 진단기
- 문항별(## 또는 문항 구분) 자동 파싱
- 공백 포함 / 미포함 글자 수 계산
- SKALA 표준 권장 범위(85% ~ 95%) 충족 판정
"""
import sys
import re

def analyze_section(title, text, limit):
    text = text.strip()
    with_spaces = len(text)
    no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", ""))
    ratio = (with_spaces / limit) * 100 if limit > 0 else 0
    
    status = "OK" if 85.0 <= ratio <= 95.0 else ("SHORT" if ratio < 85.0 else "OVER")
    print(f"\n[{title}] (제한: {limit}자)")
    print(f"  - 공백 포함: {with_spaces}자 ({ratio:.1f}%)")
    print(f"  - 공백 제외: {no_spaces}자")
    print(f"  - 권장 분량 (85~95%): {int(limit*0.85)}자 ~ {int(limit*0.95)}자")
    print(f"  - 판정: [{status}]", end=" ")
    if status == "SHORT":
        print(f"-> {int(limit*0.85) - with_spaces}자 보강 필요")
    elif status == "OVER":
        print(f"-> {with_spaces - int(limit*0.95)}자 축소 필요")
    else:
        print("-> SKALA 표준 엄수 완료 (최적 분량)")
    return with_spaces, ratio

def parse_and_analyze(content, default_limit=800):
    print("=" * 60)
    print("   SKALA 자기소개서 문항별 글자 수 정밀 진단")
    print("=" * 60)
    
    # Split by markdown headers
    sections = re.split(r"(^##+ .+)", content, flags=re.MULTILINE)
    if len(sections) > 1:
        current_title = "도입부"
        for part in sections:
            part = part.strip()
            if not part: continue
            if part.startswith("#"):
                current_title = part.lstrip("#").strip()
            else:
                # Extract limit from title if available e.g. (800자)
                m = re.search(r"(\d{3,4})자", current_title)
                limit = int(m.group(1)) if m else default_limit
                analyze_section(current_title, part, limit)
    else:
        analyze_section("전체 문안", content, default_limit)
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        lim = int(sys.argv[2]) if len(sys.argv) > 2 else 800
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        parse_and_analyze(content, lim)
    else:
        print("Usage: python char_counter.py <file_path> [default_limit]")
