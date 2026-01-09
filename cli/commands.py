from core.matrixGraph import *
from core.listGraph import *
from core.rumor import *
from utils.randomPeople import *
from utils.peopleIO import *
from math import log
import random
import logging

logger = logging.getLogger(__name__)

# TODO: Make commands take in the interface and access/mutate people as sim object attributes

def reload_all_people(interface):
    interface.sim.reload_all_people()

def _update_present_names(interface, person, action):
    interface.sim.update_present_names(person, action)


def _resolve_person(interface, name_str, name_index):
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

    # If only first name given
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

    # If full name given
    key = (fname, lname)
    if key not in name_index:
        raise ValueError(f"No person found with name '{fname} {lname}'.")

    return name_index[key]


def _find_keys_by_fname(interface, name_index, fname):
    fname = fname.lower()
    return [
        person
        for (first, last), person in interface.sim.all_name_index.items()
        if first == fname
    ]


def add_person(interface, graphs, name_str):
    person = _resolve_person(interface, name_str, interface.sim.all_name_index)

    # Add to graphs
    for g in graphs.values():
        g.add_vertex(person)

    _update_present_names(interface, person, "add")

    logger.info(f"{person} successfully added!")


def remove_person(interface, graphs, name_str):
    person = _resolve_person(interface, name_str, interface.sim.present_name_index)
    # Remove the person from each graph
    for graph in graphs.values():
        graph.remove_vertex(person)

    # Remove from working name index
    _update_present_names(interface, person, "remove")

    logger.info(f"{person} successfully removed.")


def generate_people(interface, graphs, number, location = "generated_set"):
    number = int(number)
    if number > 5000:
        raise ValueError(f"Too many people to generate. Number must be five thousand or less, got {number}")
    new_people = build_set(number, location)
    save_people(f"assets/people/{location}.json", new_people)

    interface.sim.all_people.extend(new_people)

    logger.info(f"{number} people successfully generated!")


def connect(interface, graphs, a, b, weight = None):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    # Check which type of graph is used for friends, then add edge
    if type(graphs["friends"]) == UndirectedMatrixGraph or type(graphs["friends"]) == UndirectedListGraph:
        graphs["friends"].add_edge(a, b)
        logger.info(f"{a} and {b} are now friends!")

    else:
        if not weight:
            weight = 1.5
        graphs["friends"].add_edge(a, b, weight)

        if weight > 1.5:
            logger.info(f"{a} and {b} are now friends!")
        elif weight < 1.5:
            logger.info(f"{a} and {b} are now enemies.")
        else:
            logger.info(f"{a} and {b} are now acquainted.")

        _set_trust(interface, graphs, a, b, weight)


def disconnect(interface, graphs, a, b):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    graphs["friends"].remove_edge(a, b)

    logger.info(f"{a} and {b} are no longer acquainted.")


def strengthen_edge(interface, graphs, a, b, weight):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 2.0:
        logger.info(f"{a} and {b} are already best friends!")
        return

    graphs["friends"].strengthen_edge(a, b, weight)
    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 2.0:
        logger.info(f"{a} and {b} are now best friends!")
    elif friendship == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif friendship > 1.5:
        logger.info(f"{a} and {b} are now better friends!")
    else:
        logger.info(f"{a} and {b} still dislike each other.")


def weaken_edge(interface, graphs, a, b, weight):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 1.0:
        logger.info(f"{a} and {b} already despise each other.")
        return

    graphs["friends"].weaken_edge(a, b, weight)
    friendship = graphs["friends"].get_edge(a, b)

    if friendship == 1.0:
        logger.info(f"{a} and {b} are now arch-enemies.")
    elif friendship == 1.5:
        logger.info(f"{a} and {b} have a neutral relationship.")
    elif friendship < 1.5:
        logger.info(f"{a} and {b} now dislike each other more.")
    else:
        logger.info(f"{a} and {b} still like each other.")


def strengthen_trust(interface, graphs, a, b, weight = None):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    if not weight:
        weight = 1.0

    trust = graphs["trust"].get_edge(a, b)

    if trust == 0:
        raise ValueError(f"{a} and {b} don't know each other.")

    if trust == 2.0:
        logger.info(f"{a} already trusts {b} completely!")
        return

    graphs["trust"].strengthen_edge(a, b, weight)
    trust = graphs["trust"].get_edge(a, b)

    if trust == 2.0:
        logger.info(f"{a} now trusts {b} completely!")
    elif trust > 1.4 and trust < 1.6:
        logger.info(f"{a} has neutral trust toward {b}.")
    elif trust <= 1.4:
        logger.info(f"{a} still doesn't trust {b} much.")
    else:
        logger.info(f"{a} trusts {b}.")
        

def weaken_trust(interface, graphs, a, b, weight = None):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

    if not weight:
        weight = 1.0

    trust = graphs["trust"].get_edge(a, b)

    if trust == 0:
        raise ValueError(f"{a} and {b} don't know each other.")

    '''
    if trust == 0:
        weight = 1.5 - weight
        weight = clip(weight, 1.0, 2.0)
        _set_trust(interface, a, b)
    '''

    if trust == 1.0:
        logger.info(f"{a} already doesn't trust {b} at all.")
        return

    graphs["trust"].weaken_edge(a, b, weight)
    trust = graphs["trust"].get_edge(a, b)

    if trust == 1.0:
        logger.info(f"{a} now doesn't trust {b} at all.")
    elif trust > 1.4 and trust < 1.6:
        logger.info(f"{a} has neutral trust toward {b}.")
    elif trust <= 1.4:
        logger.info(f"{a} doesn't trust {b} much.")
    else:
        logger.info(f"{a} still trusts {b}.")


def _set_trust(interface, graphs, a, b, weight):
    a = _resolve_person(interface, a, interface.sim.present_name_index)
    b = _resolve_person(interface, b, interface.sim.present_name_index)

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
    trust = min(max(trust_noisy_a, 1.05), 1.95)
    graphs["trust"].add_edge(a, b, trust)

    # Mirror last step for other direction
    trust_noisy_b = trust_raw + random.uniform(-e, e)
    trust = min(max(trust_noisy_b, 1.05), 1.95)
    graphs["trust"].add_edge(b, a, trust)

    logger.info(f"{a} trust for {b} = " + str(graphs["trust"].get_edge(a,b)))
    logger.info(f"{b} trust for {a} = " + str(graphs["trust"].get_edge(b,a)))


def spread_rumor(interface, graphs, spreader, target, rumor: str):
    spreader = _resolve_person(interface, spreader, interface.sim.present_name_index)
    target = _resolve_person(interface, target, interface.sim.present_name_index)

    rumor = Rumor(graphs["friends"], spreader, target, rumor)
    rumor.spread_rumor()

    logger.info(f"\n{spreader} spread a rumor about {target} to {len(rumor)} people!\n")
    logger.info(str(rumor.summary()) + "\n")

    return rumor


def start_sim(sim):
    logger.info("Simulation started!\n")
    sim.start()

def stop_sim(sim):
    if not sim.timer.isActive():
        logger.info("Simulation not running.\n")
        return
    sim.stop()
    logger.info("Simulation stopped!\n")

def sim_tick(sim):
    sim.step_once()
    logger.info("Simulation stepped forward by one tick!\n")

def set_sim_speed(sim, interval):
    interval = float(interval)
    sim.set_tick_interval(interval)
    logger.info(f"Simulation tick speed set to ~{round(interval, 2)} seconds per tick. (~{round(1/interval, 2)} ticks/second)\n")


def print_rumors(rumors):
    if len(rumors) < 1:
        logger.info("No rumors to show.\n")
        return
    logger.info("")
    for i in rumors:
        logger.info(i)
    logger.info("")


def change_view(interface, graphs, mode: str):
    page = 0
    already_set = False
    if mode == "friends":
        if interface.view.page == 0:
            already_set = True
        else:
            interface.view.page = 0
    elif mode == "gossip":
        if len(interface.sim.rumors) < 1:
            raise ValueError("No gossip to track.")
        if interface.view.page == 1:
            already_set = True
        else:
            interface.view.page = 1
    elif mode == "trust":
        if interface.view.page == 2:
            already_set = True
        else:
            interface.view.page = 2
    else:
        raise ValueError(f"Incorrect view mode entered. Options: friends, gossip, trust. Entered: {mode}")

    if already_set:
        raise ValueError(f"View {mode} mode already active.")
    


def print_people(graphs):
    people = graphs["friends"].get_vertices()

    logger.info("\nAll people present:\n")
    for person in people:
        if person:
            logger.info(f"    {person}")
    logger.info("")


def help_user(graphs, commands, query = None):
    if query:
        if query in commands:
            match query:
                case "person":
                    logger.info("Adds a person from the local database by name. Takes one argument.")
                case "people":
                    logger.info("Lists all people present in the simulation. Takes zero arguments.")
                case "kill":
                    logger.info("Removes a person from the simulation. Takes one argument.")
                case "help":
                    logger.info("Prints all available commands if given no arguments. Prints details of a command if given the command as an argument. Takes one-two arguments.")
                case "generate":
                    logger.info("Creates x (int) new people by calling the Randomuser.me API. Takes on argument.")
                case "reload":
                    logger.info("Reloads the simulation's internal person registry from given file in assets/people. Uses default location if no argument is given. Takes zero-one argument.")
                case "connect":
                    logger.info("Connects two people. Weight can be given as a third argument if using a weighted graph, but will default to neutral otherwise. Takes two-three arguments.")
                case "disconnect":
                    logger.info("Disconnects two people. Takes two arguments.")
                case "strengthen":
                    logger.info("Increases friendship level between two people. Any number (float) >= 1 will always max friendship level. Takes three arguments.")
                case "weaken":
                    logger.info("Decreases friendship level between two people. Any number (float) >= 1 will always min friendship level. Takes three arguments.")
                case "trust":
                    logger.info("Increases trust level of first person for second person. Any number (float) >= 1 will always max trust level. Takes three arguments.")
                case "distrust":
                    logger.info("Decreases trust level of first person for second person. Any number (float) >= 1 will always min trust level. Takes three arguments.")
                case "spread":
                    logger,info("Spreads a rumor: First argument is the name of the spreader, second is the name of the target of the rumor, and third is the string representing the contents of the rumor.")
                case "rumors":
                    logger.info("Prints full history of rumors in simulation instance. Takes zero arguments.")
                case "view":
                    logger.info("Takes on argument: 'friends' to see friendships, 'gossip' to see the latest rumor, and 'trust' to see trust levels")
                case _:
                    raise ValueError(f"help: command '{query}' not found.")
        else:
            raise ValueError(f"help: command '{query}' not found.")
        logger.info("")

    else:
        COMMAND_ORDER = [
            "help", "generate", "reload", "people", "person", "kill",
            "connect", "disconnect",
            "strengthen", "weaken",
            "trust", "distrust",
            "spread", "rumors",
            "view"
        ]
        # Print the commands that are available based on graphs
        logger.info("\nAvailable commands:\n")
        for cmd in COMMAND_ORDER:
            if cmd in commands:
                logger.info(f"    {cmd}")
        logger.info("")