from pathlib import Path

import pandas as pd

INPUT_DIR = Path("input_files")
OUTPUT_DIR = Path("output_files")

# Row (0-based) where the column names are, for each Excel file
HEADER_ROWS = {
    "BSCT": 4,
    "Morphe": 1,
}


def excel_to_csv(excel_file: Path, header_row: int) -> Path:
    # dtype=str keeps values as written in Excel (e.g. room "001" stays "001")
    df = pd.read_excel(excel_file, header=header_row, dtype=str)

    # Column names in Morphe have trailing spaces ("ROOMS     ")
    df.columns = df.columns.str.strip()

    # Morphe: keep only the rooms, stop at the "Total" row (statistics below)
    if "Name" in df.columns:
        total_rows = df.index[df["Name"].str.strip() == "Total"]
        if len(total_rows) > 0:
            df = df.loc[: total_rows[0] - 1]

    # Remove empty columns/rows (merged cells in Excel leave empty columns)
    df = df.dropna(axis="columns", how="all")
    df = df.dropna(axis="index", how="all")

    csv_file = OUTPUT_DIR / f"{excel_file.stem}.csv"
    df.to_csv(csv_file, index=False)
    return csv_file


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    for name, header_row in HEADER_ROWS.items():
        excel_file = INPUT_DIR / f"{name}.xlsx"
        csv_file = excel_to_csv(excel_file, header_row)
        print(f"{excel_file} -> {csv_file}")


if __name__ == "__main__":
    main()
