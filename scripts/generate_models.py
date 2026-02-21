#!/usr/bin/env python3
"""openapi.json → _generated.py の自動生成スクリプト。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "openapi.json"
OUTPUT = ROOT / "src" / "gbizinfo" / "models" / "_generated.py"


def main() -> None:
    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input",
        str(INPUT),
        "--output",
        str(OUTPUT),
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--input-file-type",
        "openapi",
        "--target-python-version",
        "3.12",
        "--use-standard-collections",
        "--use-union-operator",
        "--field-constraints",
        "--capitalise-enum-members",
        "--use-field-description",
        "--strict-nullable",
        "--base-class",
        "gbizinfo.models._base.BaseModel",
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(result.returncode)

    # OpenAPI spec の kana パターンは ー（長音符）を含まず実データと不整合のため除去
    content = OUTPUT.read_text(encoding="utf-8")
    content = content.replace(
        "pattern='^[ァ-ヶ]*$'",
        "",
    )
    # 空引数のカンマ整理 (e.g. "Field(None, max_length=200, min_length=0, )")
    import re
    content = re.sub(r",\s*\)", ")", content)
    OUTPUT.write_text(content, encoding="utf-8")

    # ハイフン alias 検証
    required_aliases = ["hojin-infos", "corporation-info", "meta-data"]
    for alias in required_aliases:
        if alias not in content:
            print(f"WARNING: alias '{alias}' not found in generated output")
        else:
            print(f"OK: alias '{alias}' found")

    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()
