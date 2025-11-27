from core.matrixGraph import *
from utils.randomPeople import *
from utils.peopleIO import *
from math import log
from numpy import random
from numpy import clip
import logging

logger = logging.getLogger(__name__)

all_people = load_people("assets/people/generated_set.json")
name_index = {
    (p.data.fname.lower(), p.data.lname.lower()): p
    for p in all_people
}

def _resolve_person(name_str):
    # If already a Person object, just return it
    if isinstance(name_str, Person):
        return name_str

    tokens = name_str.strip().split()

    if len(tokens) == 0:
        raise ValueError("No name provided.")

    # First token = first name
    fname = tokens[0].lower()

    # Everything else = last name
    lname = None
    if len(tokens) > 1:
        lname = " ".join(tokens[1:]).lower()

    # --- Case 1: Only first name given ---
    if lname is None:
        matches = [
            person
            for (f, l), person in name_index.items()
            if f == fname
        ]

        if len(matches) == 0:
            raise ValueError(f"No person found with first name '{fname}'.")

        if len(matches) > 1:
            msg = "Multiple people found:\n"
            for p in matches:
                msg += f"   {p}\n"
            msg += "Provide full name to disambiguate."
            raise ValueError(msg)

        return matches[0]

    # --- Case 2: Full name given ---
    key = (fname, lname)
    if key not in name_index:
        raise ValueError(f"No person found with name '{fname} {lname}'.")

    return name_index[key]


def add_person(graphs, name_str):
    person = _resolve_person(name_str)

    # Add to graphs
    for g in graphs.values():
        g.add_vertex(person)

    logger.info(f"{person} successfully added!")


def remove_person(graphs, name_str):
    person = _resolve_person(name_str)
    # Remove the person from each graph
    for graph in graphs.values():
        graph.remove_vertex(person)

    logger.info(f"{person} successfully removed.")


def _find_keys_by_fname(name_index, fname):
    fname = fname.lower()
    return [
        person
        for (first, last), person in name_index.items()
        if first == fname
    ]


def generate_people(graphs, number):
    number = int(number)
    new_people = build_set(number)
    save_people("assets/people/generated_set.json", new_people)
    all_people.append(new_people)

    logger.info(f"{number} people successfully generated!")


def connect(graphs, a, b, weight = None):
    a = _resolve_person(a)
    b = _resolve_person(b)

    # Check which type of graph is used for friends, then add edge
    if isinstance(graphs["friends"], U_MatrixGraph):
        graphs["friends"].add_edge(a, b)
        logger.info(f"{a} and {b} are now friends!")

    else:
        graphs["friends"].add_edge(a, b, weight)

        if weight > 1.5:
            logger.info(f"{a} and {b} are now friends!")
        elif weight < 1.5:
            logger.info(f"{a} and {b} are now enemies.")
        else:
            logger.info(f"{a} and {b} are now acquainted.")

        _set_trust(graphs, a, b, weight)


def disconnect(graphs, a, b):
    a = _resolve_person(a)
    b = _resolve_person(b)

    graphs["friends"].remove_edge(a, b)

    logger.info(f"{a} and {b} are no longer acquainted.")


def strengthen_edge(graphs, a, b, weight):
    a = _resolve_person(a)
    b = _resolve_person(b)

    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 2.0:
        logger.info(f"{a} and {b} are already best friends!")
        return

    graphs["friends"].strengthen_edge(a, b, weight)

    if friendship == 2.0:
        logger.info(f"{a} and {b} are now best friends!")
    elif friendship == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif friendship > 1.5:
        logger.info(f"{a} and {b} are now better friends!")
    else:
        logger.info(f"{a} and {b} still dislike each other.")


def weaken_edge(graphs, a, b, weight):
    a = _resolve_person(a)
    b = _resolve_person(b)

    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 1.0:
        logger.info(f"{a} and {b} already despise each other.")
        return

    graphs["friends"].weaken_edge(a, b, weight)

    if friendship == 1.0:
        logger.info(f"{a} and {b} are now arch-enemies.")
    elif friendship == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif friendship < 1.5:
        logger.info(f"{a} and {b} now dislike each other more.")
    else:
        logger.info(f"{a} and {b} still like each other.")


def strengthen_trust(graphs, a, b, weight = None):
    a = _resolve_person(a)
    b = _resolve_person(b)

    if not weight:
        weight = 1.0

    trust = graphs["trust"].get_edge(a, b)

    if trust == 0:
        raise ValueError(f"{a} and {b} don't know each other.")


    if trust == 2.0:
        logger.info(f"{a} already trusts {b} completely!")
        return

    graphs["trust"].strengthen_edge(a, b, weight)

    if trust == 2.0:
        logger.info(f"{a} now trusts {b} completely!")
    elif trust > 1.4 and trust < 1.6:
        logger.info(f"{a} has neutral trust toward {b}.")
    elif trust <= 1.4:
        logger.info(f"{a} still doesn't trust {b} much.")
    else:
        logger.info(f"{a} trusts {b}.")
        

def weaken_trust(graphs, a, b, weight = None):
    a = _resolve_person(a)
    b = _resolve_person(b)

    if not weight:
        weight = 1.0

    trust = graphs["trust"].get_edge(a, b)

    if trust == 0:
        raise ValueError(f"{a} and {b} don't know each other.")

    if trust == 0:
        weight = 1.5 - weight
        weight = clip(weight, 1.0, 2.0)
        _set_trust(a, b)

    if trust == 1.0:
        logger.info(f"{a} already doesn't trust {b} at all.")
        return

    graphs["trust"].weaken_edge(a, b, weight)

    if trust == 1.0:
        logger.info(f"{a} now doesn't trust {b} at all.")
    elif trust > 1.4 and trust < 1.6:
        logger.info(f"{a} has neutral trust toward {b}.")
    elif trust <= 1.4:
        logger.info(f"{a} doesn't trust {b} much.")
    else:
        logger.info(f"{a} still trusts {b}.")


def _set_trust(graphs, a, b, weight):
    a = _resolve_person(a)
    b = _resolve_person(b)

    # Initialize variables for randomness (e) and log shape knob (k)
    e = 0.05
    k = 4

    # Convert weight to -1 -> +1 scale
    relative = (weight - 1.5) / 0.5

    # Capture sign and magnitude
    sign = 1 if relative >= 0 else -1
    mag  = abs(relative)

    # Apply soft logarithmic curve and reapply sign
    curved_mag = log(1 + k * mag) / log(1 + k)
    curved = sign * curved_mag

    # Map from [-1, +1] to [1, 2]
    trust_raw = 1.5 + 0.5 * curved

    # Apply slight randomness, restrain max/min. and add to graph
    trust_noisy_a = trust_raw + random.uniform(-e, e)
    trust = clip(trust_noisy_a, 1.05, 1.95)
    graphs["trust"].add_edge(a, b, trust)

    # Mirror last step for other direction
    trust_noisy_b = trust_raw + random.uniform(-e, e)
    trust = clip(trust_noisy_b, 1.05, 1.95)
    graphs["trust"].add_edge(b, a, trust)

    logger.info(f"{a} trust for {b} = " + str(graphs["trust"].get_edge(a,b)))
    logger.info(f"{b} trust for {a} = " + str(graphs["trust"].get_edge(b,a)))


def print_people(graphs):
    people = graphs["friends"].vertices

    logger.info("\nAll people present:\n")
    for person in people:
        logger.info(f"    {person}")
    logger.info("")


def help_user(graphs, commands):
    # Print the commands that are available based on graphs
    logger.info("\nAvailable commands:\n")
    for cmd in sorted(commands):
        logger.info(f"    {cmd}")
    logger.info("")