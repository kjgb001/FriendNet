import json
from pathlib import Path
from core.node import Identity, Person
import logging

logger = logging.getLogger(__name__)

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
    except (FileNotFoundError, json.JSONDecodeError) as e:
        info = None
        if isinstance(e, json.JSONDecodeError):
            logging.info("Could not read JSON file.")
        elif isinstance(e, FileNotFoundError):
            logging.info("File does not exist.")
        data = []

    people = []
    if len(data) == 0:
        return False
    for entry in data:
        identity = Identity(entry["fname"], entry["lname"], entry["gender"], entry["picture"])
        people.append(Person(identity))
    return people