#!/usr/bin/env python3
"""data/sources/000925835.xls → _municipality.py の自動生成スクリプト。"""

from __future__ import annotations

import textwrap
from pathlib import Path

import xlrd  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "sources" / "000925835.xls"
OUTPUT = ROOT / "src" / "gbizinfo" / "enums" / "_municipality.py"


def main() -> None:
    wb = xlrd.open_workbook(str(INPUT))
    sh = wb.sheet_by_index(0)

    entries: list[tuple[str, str, str, str, str]] = []
    for row_idx in range(1, sh.nrows):
        raw_code = sh.cell_value(row_idx, 0)
        if isinstance(raw_code, float):
            code = str(int(raw_code)).zfill(6)
        else:
            code = str(raw_code).strip().zfill(6)

        if not code or not code.isdigit():
            continue

        pref_name = str(sh.cell_value(row_idx, 1)).strip()
        city_name = str(sh.cell_value(row_idx, 2)).strip()
        pref_kana = str(sh.cell_value(row_idx, 3)).strip()
        city_kana = str(sh.cell_value(row_idx, 4)).strip()

        if not pref_name:
            continue

        entries.append((code, pref_name, city_name, pref_kana, city_kana))

    lines = []
    lines.append(textwrap.dedent('''\
        """全国地方公共団体コード（自動生成 - 編集禁止）。

        scripts/generate_municipality.py から data/sources/000925835.xls を読み込んで生成。
        """

        from __future__ import annotations

        from typing import NamedTuple, NewType

        MunicipalityCode = NewType("MunicipalityCode", str)
        """全国地方公共団体コード（6桁文字列）。"""


        class MunicipalityEntry(NamedTuple):
            """地方公共団体の情報。"""

            code: MunicipalityCode
            prefecture_name: str
            city_name: str
            prefecture_name_kana: str
            city_name_kana: str

            @property
            def prefecture_code(self) -> str:
                """都道府県コード（先頭2桁）。"""
                return self.code[:2]


        _MUNICIPALITIES: dict[str, MunicipalityEntry] = {
    '''))

    for code, pref, city, pref_k, city_k in entries:
        pref_esc = pref.replace('"', '\\"')
        city_esc = city.replace('"', '\\"')
        pref_k_esc = pref_k.replace('"', '\\"')
        city_k_esc = city_k.replace('"', '\\"')
        lines.append(
            f'    "{code}": MunicipalityEntry(MunicipalityCode("{code}"), '
            f'"{pref_esc}", "{city_esc}", "{pref_k_esc}", "{city_k_esc}"),'
        )

    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append(textwrap.dedent('''\
        def get_municipality(code: str) -> MunicipalityEntry | None:
            """団体コードから検索。"""
            return _MUNICIPALITIES.get(code)


        def find_municipalities(
            *,
            prefecture: str | None = None,
            name: str | None = None,
        ) -> list[MunicipalityEntry]:
            """都道府県名や市区町村名で部分一致検索。"""
            results: list[MunicipalityEntry] = []
            for entry in _MUNICIPALITIES.values():
                if prefecture and prefecture not in entry.prefecture_name:
                    continue
                if name and name not in entry.city_name and name not in entry.prefecture_name:
                    continue
                results.append(entry)
            return results
    '''))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {len(entries)} entries → {OUTPUT}")


if __name__ == "__main__":
    main()
