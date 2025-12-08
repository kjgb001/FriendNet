import json
from pathlib import Path
from core.node import Identity, Person

def save_people(path: str, people: list):
    file_path = Path(path)

    # Check if file already exists
    try:
        existing = json.loads(file_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    # Add new entries
    for p in people:
        existing.append({
            "fname": p.data.fname,
            "lname": p.data.lname,
            "gender": p.data.gender,
            "picture": p.data.picture
        })

    # Dump to json file
    file_path.write_text(json.dumps(existing, indent=4))


def load_people(path: str) -> list:
    file_path = Path(path)
    try:
        data = json.loads(file_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        print("Could not read JSON file. Is it empty, was it manually edited?")
        data = []

    people = []
    for entry in data:
        identity = Identity(entry["fname"], entry["lname"], entry["gender"], entry["picture"])
        people.append(Person(identity))
    return people