import csv
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from final import main


st.title("소장칩 실험 기록 점검기")
st.write("CSV를 올리면 기포나 누수가 기록된 칩을 확인할 수 있습니다.")

uploaded_file = st.file_uploader("검사할 CSV 파일", type=["csv"])

if uploaded_file is not None:
    try:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            report_path = Path(temp_dir) / "report.txt"

            input_path.write_bytes(uploaded_file.getvalue())
            main(input_path, report_path)
            report = report_path.read_text(encoding="utf-8")
    except (OSError, ValueError, csv.Error) as error:
        st.error(f"오류: {error}")
    else:
        st.text(report)
        st.download_button(
            "보고서 다운로드",
            data=report.encode("utf-8"),
            file_name="chip_report.txt",
            mime="text/plain",
        )