import csv
import sys
from pathlib import Path


def main(input_path, output_path):
    abnormal_records = []

    with input_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file)

        if next(reader, None) != ["칩ID", "기포", "누수"]:
            raise ValueError("첫 줄은 칩ID,기포,누수여야 합니다.")

        for row_number, row in enumerate(reader, start=2):
            if len(row) != 3:
                raise ValueError(f"{row_number}행: 값이 3개여야 합니다.")

            chip_id, bubble, leak = (value.strip() for value in row)

            if not chip_id:
                raise ValueError(f"{row_number}행: 칩ID가 비어 있습니다.")
            if bubble not in ("있음", "없음") or leak not in ("있음", "없음"):
                raise ValueError(f"{row_number}행: 기포와 누수는 '있음' 또는 '없음'이어야 합니다.")

            reasons = []
            if bubble == "있음":
                reasons.append("기포")
            if leak == "있음":
                reasons.append("누수")

            if reasons:
                abnormal_records.append(f"{chip_id} - {', '.join(reasons)}")

    report_lines = [f"이상 기록: {len(abnormal_records)}건", *abnormal_records]
    report = "\n".join(report_lines)
    output_path.write_text(report + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python basic.py 입력.csv 보고서.txt", file=sys.stderr)
        sys.exit(2)

    try:
        main(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError, csv.Error) as error:
        print(f"오류: {error}", file=sys.stderr)
        sys.exit(1)