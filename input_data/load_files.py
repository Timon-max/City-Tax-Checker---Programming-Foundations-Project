# US-1: Load the two lists
import csv 
from pathlib import Path
from config import BSCT_COLUMNS, MORPHE_COLUMNS


def ask_file_path(list_name):
    while True:
        text = input(f"Path to the {list_name} file : ").strip()
        path = Path(text)

        if path.suffix.lower() != ".csv":
            print("Only .csv files are supported")
        elif not path.is_file():
            print(f"File not found: {path}")
        else:
            return path
        

def read_csv_file(path, required_columns=()):
    with open(path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        if reader.fieldnames is None or len(reader.fieldnames) < 2:
            raise ValueError("wrong separator, expected ';'")

        missing = []
        for column in required_columns:
            if column not in reader.fieldnames:
                missing.append(column)

        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")
        rows = list(reader)
    return rows


def load_list(list_name, required_columns=()):
    while True:
        path = ask_file_path(list_name)
        try:
            rows = read_csv_file(path, required_columns)
        except (ValueError, OSError) as error:
            print(f"{path.name}: {error}")
        else:
            return rows


def load_both_lists():
    bsct = load_list("BSCT", BSCT_COLUMNS)
    print(f"BSCT loaded: {len(bsct)} rows")
    morphe = load_list("Morphe", MORPHE_COLUMNS)
    print(f"Morphe loaded: {len(morphe)} rows")
    return bsct, morphe


if __name__ == "__main__":
    bsct, morphe = load_both_lists()
    print(bsct[0])
    print(morphe[0])
