# HealingArty Prompt Randomizer V11 🎨

### 🇰🇷 한국어

ComfyUI용 랜덤 프롬프트 생성 노드입니다. 클릭 한 번으로 고퀄리티 프롬프트를 자동으로 조합해줍니다.

#### ✨ 주요 기능
- **100+ 헤어스타일**: `fishtail braid`, `wolf cut`, `jellyfish cut`, `wet look` 등 트렌디 헤어 포함
- **의상/란제리/수영복**: 수백 개 옵션 지원, `random` 선택시 자동 랜덤
- **가로&세로 포즈 분리**: 가로 구도용 포즈, 세로 구도용 포즈를 따로 관리해서 비율에 맞는 포즈 랜덤 생성
- **가중치 시스템**: 자주 쓰고 싶은 카테고리는 가중치 0.1~2.0으로 확률 조절
- **시드 고정**: 같은 시드값으로 결과 재현 가능
- **표정/분위기/장소/소품**: 1girl 사진 프롬프트에 필요한 요소 전부 포함

<img width="335" height="721" alt="HealingArty V11" src="https://github.com/user-attachments/assets/6e17094e-c0d2-4566-bbcf-f9029048f40e" />

#### 🚀 설치 방법
1. ComfyUI `custom_nodes` 폴더로 이동
```bash
cd ComfyUI/custom_nodes
Bash
git clone https://github.com/daning1212/HealingaArty_prompt_randomizer.git
ComfyUI 재시작
🔄 업데이트 방법
Bash
cd ComfyUI/custom_nodes/HealingaArty_prompt_randomizer
git pull
ComfyUI 재시작

📝 사용법
빈 캔버스 더블클릭 → heal 검색 → HealingArty Prompt Randomizer V11 추가
또는 우클릭 → Add Node → HealingArty → HealingArty Prompt Randomizer V11
원하는 카테고리 random으로 설정하거나 직접 선택
positive_prompt 출력을 CLIP Text Encode에 연결
⚙️ 주요 옵션
옵션

설명

시드

-1이면 완전랜덤, 숫자 입력시 결과 고정

랜덤_모드

완전랜덤 / 고정

헤어스타일

none, random, 또는 직접 선택

의상/란제리/수영복

none, random, 또는 직접 선택

세로포즈

세로 구도에 맞는 포즈 리스트

가로포즈

가로 구도에 맞는 포즈 리스트

xx_가중치

0.1∼2.0, 높을수록 해당 태그 우선 출력

추가_태그

high quality, detailed 등 고정으로 붙일 태그

📌 출력
positive_prompt: 조합된 프롬프트 문자열
세부사항: 사용된 옵션 + 시드값
사용된_시드: 실제 적용된 시드
⚠️ 주의사항
폴더명은 HealingaArty_prompt_randomizer로 a가 하나 더 들어갔습니다. 기존 설치 호환성을 위해 유지합니다. 노드명은 HealingArty로 정상 표기됩니다.

📋 버전 히스토리
V11: buzz cut 제거, 브레이드/트렌디 헤어 20종+ 추가, 카테고리 HealingArty로 변경
V10: 초기 릴리즈


🇺🇸 English
A random prompt generator node for ComfyUI. Create high-quality prompts with one click.

✨ Features
100+ Hairstyles: Includes trendy styles like fishtail braid, wolf cut, jellyfish cut, wet look
Outfits/Lingerie/Swimwear: Hundreds of options, supports random selection
Horizontal & Vertical Poses: Separate pose lists for landscape/portrait to match aspect ratio
Weight System: Adjust probability 0.1∼2.0 for preferred categories
Seed Lock: Reproduce results with fixed seed
Expressions/Mood/Location/Props: All elements needed for 1girl photo prompts
🚀 Installation
Go to ComfyUI custom_nodes folder
Bash
cd ComfyUI/custom_nodes
Clone repository
Bash
git clone https://github.com/daning1212/HealingaArty_prompt_randomizer.git
Restart ComfyUI
🔄 Update
Bash
cd ComfyUI/custom_nodes/HealingaArty_prompt_randomizer
git pull
Restart ComfyUI

📝 Usage
Double-click canvas → search heal → add HealingArty Prompt Randomizer V11
Or right-click → Add Node → HealingArty → HealingArty Prompt Randomizer V11
Set categories to random or choose manually
Connect positive_prompt output to CLIP Text Encode
⚙️ Key Options
Option

Description

Seed

-1 for full random, input number to lock result

Random_Mode

완전랜덤 / 고정 = Full Random / Fixed

Hairstyle

none, random, or select manually

Outfit/Lingerie/Swimsuit

none, random, or select manually

Vertical_Pose

Poses for portrait aspect ratio

Horizontal_Pose

Poses for landscape aspect ratio

xx_Weight

0.1∼2.0, higher = more likely to appear

Extra_Tags

Fixed tags like high quality, detailed

📌 Outputs
positive_prompt: Combined prompt string
세부사항 = Details: Used options + seed
사용된_시드 = Used_Seed: Actual seed used
⚠️ Note
Folder name is HealingaArty_prompt_randomizer with an extra a. Kept for backward compatibility. Node name is correctly displayed as HealingArty.

📋 Changelog
V11: Removed buzz cut, added 20+ braids/trendy hairs, changed category to HealingArty
V10: Initial release
Made by @daning1212 | MIT License | Give it a ⭐ if you like it!
