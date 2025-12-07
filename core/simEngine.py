from cli.interface import Interface
from cli.parser import Parser
from utils.peopleIO import *
from core.matrixGraph import *
import random
import logging

logger = logging.getLogger(__name__)

class Simulation():
    
    def __init__(self, interface, populate):
        self.interface = interface
        self.parser = Parser()

        if populate:
            self.build_network()

    
    def build_network(self, file = "generated_set", count = 25):
        ''' 
        Randomly collects [count] people from specified file in assets/people directory, 
        then adds them to the active graphs and randomly makes connections between them.
        '''
        try:
            self.interface.suppress_output()
            # Get people from specified file and create a list of their indices
            all_people = load_people("assets/people/"+file+".json")
            indices = list(range(len(all_people)))
            picked = []

            # Efficiently selects people from the pool by index based on how many are specified with count
            random.shuffle(indices)
            selected_indices = indices[:count]
            
            # Adds the selected person objects to the picked list and calls the interface to add them to the simulation via command logic
            for i in selected_indices:
                picked.append(all_people[i])
                self.interface.handle("person", [f"{all_people[i].data.fname.lower()} {all_people[i].data.lname.lower()}"])

            # Assigns each person a number of total friends, chooses someone from the picked list, creates a randomized weight if the weighted graph is present, then connects them via command logic
            for person in picked:
                friend_num = random.randint(0, 25) # Could be replaced with an algorithm to assign number of friends on a bell curve
                friends = []

                for i in range(friend_num):
                    # Prevent self connection attempts
                    while True:
                        friend_index = random.randint(0, len(picked)-1)
                        if picked[friend_index] != person:
                            break

                    # Set weight if weighted friend graph in use
                    weight = random.random() + 1 if type(self.interface.graphs['friends']) == WU_MatrixGraph else None # Could be rewritten with a logarithmic probability curve to favor positive relationships over negative ones

                    # Make connection via interface command
                    self.interface.handle("connect", [f"{person.data.fname.lower()} {person.data.lname.lower()}", 
                        f"{picked[friend_index].data.fname.lower()} {picked[friend_index].data.lname.lower()}", weight])

            self.interface.resume_output()
            logger.info("\nNetwork build successful!")

                
        except Exception as e:
            logger.info(f"[Error] Simulation failed to generate network (either partially or fully), due to: {e}")

        
