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


def add_person(graphs, name_str):
    tokens = name_str.strip().split()

    if len(tokens) == 0:
        raise ValueError("No name provided.")

    fname = tokens[0]
    lname = None

    # Capture ENTIRE remainder as last name
    if len(tokens) > 1:
        lname = " ".join(tokens[1:])

    # CASE 1: first-name-only lookup
    if lname is None:
        matches = _find_keys_by_fname(name_index, fname)

        if len(matches) == 0:
            raise ValueError("Person not found.")

        if len(matches) > 1:
            logger.info("Multiple matches found:")
            for p in matches:
                logger.info(f"   {p}")
            logger.info("Use full name to disambiguate.")
            return

        person = matches[0]

    # CASE 2: full name lookup
    else:
        key = (fname.lower(), lname.lower())
        if key not in name_index:
            raise ValueError(f"Person '{fname} {lname}' not found.")
        person = name_index[key]

    # Add to graphs
    for g in graphs.values():
        g.add_vertex(person)

    logger.info(f"{person} successfully added!")


def remove_person(graphs, person):
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
    graphs["friends"].remove_edge(a, b)

    logger.info(f"{a} and {b} are no longer acquainted.")


def strengthen_edge(graphs, a, b, weight):

    if graphs["friends"].get_edge(a, b) == 2.0:
        logger.info(f"{a} and {b} are already best friends!")
        return

    graphs["friends"].strengthen_edge(a, b, weight)

    if graphs["friends"].get_edge(a, b) == 2.0:
        logger.info(f"{a} and {b} are now best friends!")
    elif graphs["friends"].get_edge(a, b) == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif graphs["friends"].get_edge(a, b) > 1.5:
        logger.info(f"{a} and {b} are now better friends!")
    else:
        logger.info(f"{a} and {b} still dislike each other.")


def weaken_edge(graphs, a, b, weight):

    if graphs["friends"].get_edge(a, b) == 1.0:
        logger.info(f"{a} and {b} already despise each other.")
        return

    graphs["friends"].weaken_edge(a, b, weight)

    if graphs["friends"].get_edge(a, b) == 1.0:
        logger.info(f"{a} and {b} are now arch-enemies.")
    elif graphs["friends"].get_edge(a, b) == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif graphs["friends"].get_edge(a, b) < 1.5:
        logger.info(f"{a} and {b} now dislike each other more.")
    else:
        logger.info(f"{a} and {b} still like each other.")


def strengthen_trust(graphs, a, b, weight = None):
    if not weight:
        weight = 1.0

    graphs["trust"].strengthen_edge(a, b, weight)
        

def weaken_trust(graphs, a, b, weight = None):
    if not weight:
        weight = 1.0

    graphs["trust"].weaken_edge(a, b, weight)


def _set_trust(graphs, a, b, weight):
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
    for person in sorted(people):
        logger.info(f"    {person}")
    logger.info("")


def help_user(graphs, commands):
    # Print the commands that are available based on graphs
    logger.info("\nAvailable commands:\n")
    for cmd in sorted(commands):
        logger.info(f"    {cmd}")
    logger.info("")