from cli.interface import Interface
from cli.parser import Parser
from utils.peopleIO import *
from core.matrixGraph import *
import random
import logging
import math
import traceback

logger = logging.getLogger(__name__)

class Simulation():
    
    def __init__(self, graphs, interface, population_count, 
        people_location = "generated_set"): # create new args in cli.py
        self.graphs = graphs
        self.interface = interface
        self.parser = Parser()
        self.rumors = []
        self.count = 0

        # Store all people and association indices here
        self.all_people = load_people(f"assets/people/{people_location}.json")
        self.all_name_index = {
            (p.data.fname.lower(), p.data.lname.lower()): p
            for p in self.all_people
        }
        self.present_name_index = {}

        # Pass self to interface and initialize interface valid commands (based on graphs present in self)
        self.interface.sim = self
        self.interface.command_init()

        # Bool that determines if the sim auot-populates using build_network()
        self.populate = True if population_count else False
        self.people_location = people_location
        if self.populate:
            self.count = population_count
            self.build_network(people_location) # TODO: Accept any passed file and count

        # Build image map for visualizer to pull from
        self.image_map = {
            person: person.data.picture 
            for person in self.all_people
           }

        # Initialize the view via interface. Executed last to ensure interface has the sim object and network is formed before view tries to access graphs.
        self.interface.view_init(self)

    
    def build_network(self, file = "generated_set"):
        ''' 
        Randomly collects [count] people from specified file in assets/people directory, 
        then adds them to the active graphs and randomly makes connections between them.
        '''
        try:
            count = self.count
            self.interface.suppress_output()
            # Get people from specified file and 
            all_people = load_people("assets/people/"+file+".json")

            # Checks if there are enough people for random selection (minimum of twice the chosen count), and generates the difference if not.
            if len(all_people) < count * 2 or not all_people:
                count_diff = (count * 2) - len(all_people)
                self.interface.handle("generate", [count_diff, file])
                self.interface.handle("reload")
                all_people = load_people("assets/people/"+file+".json")
                
            # Create a list of their indices
            indices = list(range(len(all_people)))
            picked = []

            # Efficiently selects people from the pool by index based on how many are specified with count
            random.shuffle(indices)
            selected_indices = indices[:count]
            
            # Adds the selected person objects to the picked list and calls the interface to add them to the simulation via command logic
            for i in selected_indices:
                self.interface.handle("person", [f"{all_people[i].data.fname.lower()} {all_people[i].data.lname.lower()}"])
            picked = list(self.graphs["friends"].get_vertices())

            # Determine who will seed clustering
            seed_count = max(5, int(len(picked) * 0.15))  # ~15% of population, 5 baseline
            seed_people = set(picked[:seed_count])

            # Assigns each person a number of total connections, chooses someone from the picked list, creates a randomized weight if the weighted graph is present, then connects them via command logic
            for person in picked:
                # Calculate number of connections with a normal distribution, then clamp values
                num_mean = 3 # Sets the mean number of connections
                num_standard_deviation = 1.5 * (num_mean / 5) # Sets deviation based on normalized mean
                friend_num = int(random.gauss(num_mean, num_standard_deviation))
                friend_num = max(1, min(friend_num, len(picked) - 1))

                friends = []

                for i in range(friend_num):
                    # Prevent self connection attempts
                    while True:
                        friend = self.pick_connection(person, picked, self.graphs["friends"], seed_people)
                        if friend != person:
                            break

                    # Set weight using a half-normal distribution split then clamp, if weighted friend graph in use
                    if type(self.graphs['friends']) == WU_MatrixGraph: 
                        if random.random() < 0.85: # Higher == More likely to be friends. Lower == More likely to be enemies.
                            # FRIEND distribution
                            weight = random.gauss(1.7, 0.1)
                        else:
                            # ENEMY distribution
                            weight = random.gauss(1.3, 0.1)

                        weight = max(1.0, min(weight, 2.0))
                    else:
                        weight = None

                    # Make connection via interface command
                    self.interface.handle("connect", [f"{person.data.fname.lower()} {person.data.lname.lower()}", 
                        f"{friend.data.fname.lower()} {friend.data.lname.lower()}", weight])
                    friends.append(picked[i])

                logger.debug(f"{person} number of connections: {len(friends)}")

            self.interface.resume_output()
            logger.info("\nNetwork build successful!")

        except Exception as e:
            logger.info(f"[Error] Simulation failed to generate network (either partially or fully), due to: {e}")
            traceback.print_exc() # DEBUG


    def pick_connection(self, person, picked, friend_graph, seed_people):
        # If person is one of the seeds set random friend
        if person in seed_people:
            return random.choice([p for p in picked if p != person])

        # Non-seeds get cluster-building behavior
        existing = set(friend_graph.get_neighbors(person))

        triadic_candidates = set()
        for f in existing:
            triadic_candidates.update(friend_graph.get_neighbors(f))

        # remove invalids
        triadic_candidates.discard(person)
        triadic_candidates -= existing

        # strong closure bias
        if triadic_candidates:
            return random.choice(list(triadic_candidates))

        # fallback: sparse cross-clique links
        return random.choice([p for p in picked if p != person])


    def reload_all_people(self, file: str = None):
        if not file:
            file = self.people_location
            
        self.all_people = load_people(f"assets/people/{file}.json")
        self.all_name_index = {
            (p.data.fname.lower(), p.data.lname.lower()): p
            for p in self.all_people
        }
        logger.info(f"People reloaded from {file}.\n")


    def update_present_names(self, person, action):
        if action.lower() == "add":
            self.present_name_index[
                (person.data.fname.lower(), person.data.lname.lower())
                                ] = person

        elif action.lower() == "remove":
            del self.present_name_index[
                (person.data.fname.lower(), person.data.lname.lower())]

        else:
            raise ValueError("(update_present_names) Invalid action.")