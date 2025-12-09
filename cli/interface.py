from .parser import Parser
from .commands import *
import logging
import traceback
import utils.logger as logger_mod

logger = logging.getLogger(__name__)

# Keys are commands, values are corresponding methods in commands.py
COMMAND_MAP = {
    "person": add_person,
    "people": print_people,
    "kill": remove_person,
    "help": help_user,
    "generate": generate_people,
    "reload": reload_all_people,

    "connect": connect,
    "disconnect": disconnect,

    "strengthen": strengthen_edge,
    "weaken": weaken_edge,

    "trust": strengthen_trust,
    "distrust": weaken_trust,

    "spread": spread_rumor,
    
    # add more commands
}

UNDIRECTED_COMMANDS = ["connect", "disconnect"]
DIRECTED_COMMANDS = ["spread"]
WEIGHTED_COMMANDS = ["strengthen", "weaken", "trust", "distrust"]
DAG_COMMANDS = []


class Interface:
    ''' CLI Interface '''
    def __init__(self, parser: Parser):
        self.parser = parser
        self.running = True
        self.sim = None

        self.commands = {"help", "people", "person", "kill", "generate", "reload"}
        

    def command_init(self):
        # Add commands based on graphs present
        if "friends" in self.sim.graphs:
            self.commands.update(UNDIRECTED_COMMANDS)
        if "gossip" in self.sim.graphs:
            self.commands.update(DIRECTED_COMMANDS)
        if "trust" in self.sim.graphs:
            self.commands.update(WEIGHTED_COMMANDS)
        # TODO: add dag once implemented


    def run(self):
        ''' Starts the interactive cli. Calls parser then handles input while running. '''
        print("\nWelcome to FriendNet! Please enter a command (type 'help' to see commands).\n")
        while self.running:
            raw = input("> ")
            command, args = self.parser.parse(raw)
            self.handle(command, args)


    def handle(self, command, args = None):
        ''' Check for command in the map. If present, retrieve value (method name in command.py)
        and call it, passing the graphs and args.'''
        # TODO: Refactor to pass interface into commands and have people live in Simulation object
        try:
            if command in self.commands:
                func = COMMAND_MAP[command]
                if command == "help":
                    func(self.sim.graphs, self.commands)
                elif command == "people":
                    func(self.sim.graphs)
                elif command == "spread":
                    self.sim.rumors.append(func(self, self.sim.graphs, *args))
                elif command == "reload":
                    func(self)
                else:
                    func(self, self.sim.graphs, *args)
            else:
                logger.info(f"Unknown command: {command}")
        except Exception as e:
            logger.info(f"[Error] {e}")
            #traceback.print_exc() # DEBUG


    def suppress_output(self):
        logger_mod.suppress_commands = True
    
    def resume_output(self):
        logger_mod.suppress_commands = False


