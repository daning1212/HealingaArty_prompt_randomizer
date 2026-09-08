# HealingArty Prompt Randomizer 🎨

ComfyUI용 프롬프트 조합 노드입니다. 기존 워크플로 호환성을 위해 V11 노드 이름과 식별자를 유지합니다.

## 설치

ComfyUI의 `custom_nodes` 폴더에서 실행합니다.

```cmd
git clone https://github.com/daning1212/HealingaArty_prompt_randomizer.git
```

ComfyUI 재시작 후 브라우저를 새로고침하세요. 노드 검색에서 `HealingArty`를 찾고 `positive_prompt`를 CLIP Text Encode에 연결합니다.

## 업데이트

설치된 `custom_nodes/HealingaArty_prompt_randomizer` 폴더의 탐색기 주소창에 `cmd`를 입력하고 실행합니다.

```cmd
git pull
```

완료 후 ComfyUI를 재시작하고 브라우저를 새로고침하세요. Git으로 설치한 폴더에서 사용할 수 있습니다. 로컬 수정으로 업데이트가 중단되면 변경 내용을 먼저 확인하세요.

## 모드

| 랜덤_모드 | 동작 |
| --- | --- |
| 완전랜덤 | 매 실행 새 시드로 자동 선택합니다. 중복될 수 있습니다. |
| 고정 | 0 이상의 같은 시드와 같은 입력으로 결과를 재현합니다. -1은 무작위입니다. |
| 순차 | random으로 설정한 각 카테고리를 차례대로 선택하고 끝에서 처음으로 돌아옵니다. |

직접 선택한 항목은 고정, `none`은 생략됩니다.

### 순차 사용법

1. `랜덤_모드`를 `순차`로 설정합니다.
2. `세로포즈` 또는 `가로포즈` 하나를 `random`, 나머지를 `none`으로 설정합니다.
3. 표정도 차례대로 바꾸려면 `표정`을 `random`으로 설정합니다.
4. 실행마다 다음 항목이 선택됩니다. `세부사항`에서 순번을 확인하세요.

`순차_시작번호`는 1부터 시작하며 목록 길이를 넘으면 순환합니다.
`순차_리셋` 숫자를 변경하면 시작번호부터 다시 시작합니다. 시작번호 변경 또는 다른 모드를 실행한 뒤 순차로 복귀해도 초기화됩니다.
순서는 노드별 메모리에 저장되어 ComfyUI 재시작이나 노드 재생성 시 초기화됩니다.
실행 실패 후 재시도에서도 이미 실행된 노드의 순서는 진행되었을 수 있습니다.
한 번의 노드 실행마다 진행하며, 이미지 배치 내부의 이미지마다 바뀌지는 않습니다.
순차 모드의 시드는 순서를 제어하지 않으며 -1 입력은 출력 시드 0으로 표시됩니다.

## 포즈와 표정

자동 포즈 선택은 가로 40종, 세로 40종의 자세·구도 전용 목록을 사용합니다.
꽃, 커피, 휴대폰, 특정 의상·장소를 자동 포즈 문구에 추가하지 않습니다.
이미지 모델 자체가 소품을 추가하는 것까지 막는 기능은 아닙니다.

기존 워크플로 호환성을 위해 예전 포즈 메뉴는 유지합니다. 직접 선택하면 소품을 포함한 기존 문구가 그대로 출력됩니다.
자동 전용 목록은 코드 상단 `PURE_POSES`에서 관리합니다.

표정은 미소, 웃음, 수줍음, 안도, 호기심, 놀람, 걱정, 슬픔, 결의, 장난기 등 다양한 얼굴 표현을 추가했습니다.

## 가중치와 출력

가중치는 선택 확률이 아니라 프롬프트 강조값입니다.
예: 1.2 → `(smiling:1.2)`. 1.0은 일반 문구입니다.
강조 해석은 연결된 텍스트 인코더와 모델에 따라 다릅니다.

| 출력 | 내용 |
| --- | --- |
| positive_prompt | 조합된 프롬프트 |
| 세부사항 | 모드, 시드, 선택 항목, 순차 순번 |
| 사용된_시드 | 실제 사용 시드 |

`추가_태그`는 마지막에 붙습니다. 모든 항목이 비면 기존 기본값 `1girl`을 출력합니다.

## 변경 사항

- 순차 모드, 시작번호와 리셋 추가
- 자동 포즈를 소품 없는 자세·구도로 분리
- 다양한 표정 추가
- 사용되지 않던 가중치를 강조 문법으로 적용
- 순차·완전랜덤 모드 캐시 무효화 처리
- 설치 및 업데이트 문서 정리

## English

ComfyUI prompt generator; the V11 node ID and display name stay unchanged.

- Full random (`완전랜덤`): fresh seed per execution; repeats are possible.
- Fixed (`고정`): deterministic for a nonnegative seed; -1 remains random.
- Sequential (`순차`): each category set to `random` advances through its list and wraps.
- Manual choices remain fixed; `none` omits a category.
- `순차_시작번호` is the one-based start. Change `순차_리셋` to restart.
- Sequence state is per node, in memory, and resets on restart/recreation. It advances per node execution, not per image in a batch.
- Automatic poses use 40 posture-only entries per orientation. Legacy manual entries remain available and may include props.
- Weights emit prompt emphasis, not selection probabilities.

Install with `git clone` in `custom_nodes`. Update with `git pull` inside the repository folder, restart ComfyUI, then refresh the browser.

## 개발 검사

```cmd
python -m unittest discover -v
```

Made by @daning1212. 폴더명의 HealingaArty 표기는 기존 설치 호환성을 위해 유지합니다.
