import requests
from core.node import Identity, Person

def create_person(fname, lname, gender, picture):
    identity = Identity(fname, lname, gender, picture)
    return Person(identity)


def generate_random_batch(size: int):
    # one request, N results
    url = f"https://randomuser.me/api/?nat=us,gb,ca,au,nz&results={size}"
    resp = requests.get(url, timeout=3)
    resp.raise_for_status()

    results = resp.json().get("results", [])
    people = []

    for entry in results:
        fname = entry["name"]["first"]
        lname = entry["name"]["last"]
        gender = entry["gender"]
        picture = entry["picture"]["thumbnail"]
        people.append(create_person(fname, lname, gender, picture))

    return people


def build_set(size: int):
    return generate_random_batch(size)

