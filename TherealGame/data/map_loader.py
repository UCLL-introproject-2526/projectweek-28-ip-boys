import os

def load_map_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Lege lijnen verwijderen
    return [line for line in lines if line.strip() != ""]
