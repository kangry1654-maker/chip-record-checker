# 소장칩 실험 기록 점검기

소장칩 실험 기록 CSV에서 기포나 누수가 있는 행을 찾아 건수와 원인을
표시하고, 텍스트 보고서로 저장합니다. 예시 CSV는 과제용 가상 데이터입니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `basic.py` | 리팩터링 전 기본판 |
| `refactored.py` | CSV 읽기와 행 변환을 Adapter로 분리한 버전 |
| `final.py` | 영어 열 이름을 추가로 지원하는 최종판 |
| `app.py` | 최종판 검사 기능을 사용하는 Streamlit 웹 화면 |
| `test_checker.py` | 세 버전의 동작과 영어 양식 지원을 확인하는 자동 검사 |
| `requirements.txt` | 웹 실행에 필요한 Streamlit 버전 |

## 실행 환경

Windows PowerShell, Python 3.13.14에서 확인했습니다.
터미널 실행과 자동 검사에는 Python 표준 라이브러리만 필요합니다.

## 터미널에서 실행 및 검사

프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
python final.py normal.csv report.txt
python test_checker.py
```

첫 명령은 이상 기록 2건(A - 기포, B - 누수)을 출력하고 `report.txt`에
같은 내용을 저장합니다. 자동 검사가 통과하면 마지막에 `OK`가 표시됩니다.

## 예시 입력

| 파일 | 예상 결과 |
|---|---|
| `normal.csv` | 이상 기록 2건 |
| `zero.csv` | 이상 기록 0건 |
| `invalid.csv` | 2행 값 오류, 새 보고서 생성 없음 |
| `normal_english.csv` | 최종판에서 이상 기록 2건 |

지원하는 열 이름은 `칩ID,기포,누수`와 `chip_id,bubble,leak`입니다.
기포와 누수 칸에는 `있음` 또는 `없음`을 입력합니다.

## 웹 화면 실행

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

브라우저가 자동으로 열리지 않으면 터미널에 표시된 `Local URL`을 엽니다.
`normal_english.csv`를 올리면 결과를 확인하고 보고서를 다운로드할 수 있습니다.
`invalid.csv`를 올리면 오류가 표시됩니다.
웹 실행을 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누릅니다.