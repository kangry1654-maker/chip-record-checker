import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
NORMAL_REPORT = "이상 기록: 2건\nA - 기포\nB - 누수\n"
ZERO_REPORT = "이상 기록: 0건\n"
VALUE_ERROR = "오류: 2행: 기포와 누수는 '있음' 또는 '없음'이어야 합니다.\n"
HEADER_ERROR = "오류: 첫 줄은 칩ID,기포,누수여야 합니다.\n"


class ChipCheckerTests(unittest.TestCase):
    def check_run(self, script, input_name, expected_report=None, expected_error=""):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.txt"
            result = subprocess.run(
                [sys.executable, script, input_name, str(output_path)],
                cwd=PROJECT_DIR,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                capture_output=True,
                encoding="utf-8",
            )

            if expected_report is None:
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, expected_error)
                self.assertFalse(output_path.exists())
            else:
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, expected_report)
                self.assertEqual(result.stderr, "")
                self.assertEqual(output_path.read_text(encoding="utf-8"), expected_report)

    def test_existing_inputs(self):
        for script in ("basic.py", "refactored.py", "final.py"):
            with self.subTest(script=script, input_name="normal.csv"):
                self.check_run(script, "normal.csv", expected_report=NORMAL_REPORT)
            with self.subTest(script=script, input_name="zero.csv"):
                self.check_run(script, "zero.csv", expected_report=ZERO_REPORT)
            with self.subTest(script=script, input_name="invalid.csv"):
                self.check_run(script, "invalid.csv", expected_error=VALUE_ERROR)

    def test_english_before_feature(self):
        self.check_run("refactored.py", "normal_english.csv", expected_error=HEADER_ERROR)

    def test_english_after_feature(self):
        self.check_run("final.py", "normal_english.csv", expected_report=NORMAL_REPORT)


if __name__ == "__main__":
    unittest.main(verbosity=2)