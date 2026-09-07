# 🎯 자기소개서 Skill
> **공채 자기소개서 작성, 진단 및 실전 클리닉 Antigravity 스킬**

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](https://github.com/google/antigravity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Humanize Korean](https://img.shields.io/badge/im--not--ai-70+-green.svg)](https://github.com/rntqkdl/skala-resume-clinic)

---

## 📌 개요 (Overview)

`해당 GIT`은 **Google Antigravity (AGY)** 환경에서 구동되는 공채 자기소개서 전문 진단 및 작성 에이전트 스킬입니다.  
70여 개 AI 번역투 및 상투어 배제 규칙(`im-not-ai`), 그리고 STAR 엔지니어링 방법론을 결합하여 서류 합격률을 극대화합니다.

---

## 🚀 빠른 시작 & 설치 (Installation)

### 1. 전역 스킬(Global Skill)로 설치 (추천)
모든 프로젝트 및 터미널 환경에서 항상 활성화할 수 있도록 글로벌 스킬 디렉터리에 클론합니다:

```bash
git clone https://github.com/rntqkdl/skala-resume-clinic.git ~/.gemini/antigravity-cli/skills/skala-resume-clinic
```

### 2. 특정 프로젝트 워크스페이스(Workspace Skill)로 설치
현재 작업 중인 리포지토리 내에서만 사용할 경우:

```bash
git clone https://github.com/rntqkdl/skala-resume-clinic.git .agents/skills/skala-resume-clinic
```

설치 후 Antigravity 세션에서 자소서 작성이나 검토를 요청하면 본 스킬이 자동으로 활성화(Progressive Disclosure)됩니다.

---

## 💎 핵심 작성 5대 철칙 (The 5 Iron Rules)

1. **철저한 두괄식 (첫 2~3줄 결론 완결)**
   - 질문에 대한 직접적 답변, 습득한 핵심 역량 키워드, 대표 정량 성과를 서두 2~3줄에 압축 배치합니다.
   - *미괄식("어린 시절부터...", "호기심을 가지고...") 도입부 즉시 배제.*
2. **소제목 공식: `[문제해결 행동 + 비교가능한 정량수치]`**
   - 감성적이거나 모호한 표현을 금지하고 대괄호 안에 엔지니어링 액션과 모수를 명시합니다.
   - *예시: `[빈도수 역수 가중치 설계로 1:907 롱테일 불균형 극복 및 30개 팀 중 1위 대상]`*
3. **타사 대체 불가능한 구체적 도메인 과제 직결**
   - 회사명을 바꾸어도 통하는 범용 문장을 배제하고, 지원 회사의 실제 기술 인프라(예: KT AICT/제조·통신 이상치 감지, 금융권 이상거래 탐지)를 타깃팅합니다.
4. **`im-not-ai` 70+ AI 클리셰 & 번역투 완전 제거**
   - `~를 통해`, `~에 있어서`, `~로 이어지는`, `중요성을 깨달았습니다`, `귀사` 등 AI 생성 냄새를 100% 필터링합니다.
   - 능동형 엔지니어링 서술어(`설계했습니다`, `구축했습니다`, `도출했습니다`, `단축했습니다`)를 엄수합니다.
5. **글자 수 85% ~ 95% 정밀 통제**
   - 결론부의 상투적인 다짐 문장(사족)을 전면 삭제하고, 확보한 분량을 엔지니어링 액션과 검증 지표에 투입합니다.
   - 800자 문항 기준 **680자 ~ 760자** 엄수.

---

## 📂 리포지토리 구조 (Repository Structure)

```
skala-resume-clinic/
├── SKILL.md                      # Antigravity 스킬 정의 및 오케스트레이션 지침
├── README.md                     # 프로젝트 안내 문서
├── LICENSE                       # MIT 라이선스
├── scripts/                      # 독립 실행형 CLI 진단 도구
│   ├── char_counter.py           # 문항별 공백 포함/제외 및 85~95% 최적 분량 검증기
│   └── ai_lint.py                # 70+ AI 번역투·클리셰·수동태 자동 탐지 린터
├── resources/                    # 데이터 사전 및 템플릿
│   ├── candidate_profile.template.json # 지원자 마스터 역량 템플릿
│   ├── candidate_profile.json          # 마스터 레퍼런스 데이터 (샘플)
│   └── ai_ban_dictionary.json         # AI 금지 표현 및 인간화 대체 표현 사전
├── references/                   # 취업캠프 컨설팅 상세 가이드
│   └── skala_clinic_guide.md     # 인사담당자 평가 루브릭 및 세션 원문
└── examples/                     # 실제 검증 완료된 합격권 공채 자소서 예시
    ├── 01_KT_SW_AI.md            # KT 대졸신입 AI/SW (800자 Q1: 742자, Q2: 708자)
    ├── 02_우리은행_IT.md          # 우리은행 IT/디지털 부문
    ├── 03_국민은행_IT디지털.md     # KB국민은행 IT/디지털 부문
    ├── 04_LGCNS_DX_Engineer.md   # LG CNS DX 엔지니어 부문
    └── 05_IBK기업은행_디지털.md    # IBK기업은행 디지털 부문
```

---

## 🛠️ CLI 검증 스크립트 사용법 (Scripts Usage)

### 1. AI 번역투 및 클리셰 린터 (`ai_lint.py`)
작성된 자소서 파일의 AI 어투, 소제목 수치 포함 여부, 능동형 서술어 비율을 즉시 채점합니다:

```bash
python scripts/ai_lint.py examples/01_KT_SW_AI.md
```

### 2. 문항별 글자 수 정밀 계산기 (`char_counter.py`)
문항 헤더를 자동으로 분할하여 공백 포함/제외 글자 수 및 85% ~ 95% 구간 충족 여부를 판정합니다:

```bash
python scripts/char_counter.py examples/01_KT_SW_AI.md 800
```

---

## 📝 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)에 따라 자유롭게 사용, 수정 및 배포할 수 있습니다.
