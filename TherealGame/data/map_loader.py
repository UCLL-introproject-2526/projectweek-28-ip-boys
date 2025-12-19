import os

def load_map_from_file(filename):
    # KEYWORD: FILE READER
    # [NL] Deze functie opent het tekstbestand dat we hebben meegegeven.
    # [NL] Vervolgens leest hij het bestand regel voor regel in en verwijdert hij witregels aan het einde.
    # [NL] Het resultaat is een lijst van strings die we kunnen gebruiken om het level op te bouwen.
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Lege lijnen verwijderen
    return [line for line in lines if line.strip() != ""]