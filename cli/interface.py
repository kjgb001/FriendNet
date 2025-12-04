from .parser import Parser
from .commands import *
import logging

logger = logging.getLogger(__name__)

# Keys are commands, values are corresponding methods in commands.py
COMMAND_MAP = {
    "person": add_person,
    "people": print_people,
    "kill": remove_person,
    "help": help_user,
    "generate": generate_people,

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
DIRECTED_COMMANDS = []
WEIGHTED_COMMANDS = ["strengthen", "weaken", "trust", "distrust"]
DAG_COMMANDS = []


class Interface:
    ''' CLI Interface '''
    def __init__(self, graphs: dict, parser: Parser):
        # Takes graph dict from cli.py to define which graph structures to use
        self.graphs = graphs
        self.parser = parser
        self.running = True
        self.rumors = []
        #print("DEBUG", self.graphs)

        self.commands = {"help", "people", "person", "kill", "generate"}
        # Add commands based on graphs present
        if "friends" in self.graphs:
            self.commands.update(UNDIRECTED_COMMANDS)
        if "gossip" in self.graphs:
            self.commands.update(DIRECTED_COMMANDS)
        if "trust" in self.graphs:
            self.commands.update(WEIGHTED_COMMANDS)
        # TODO: add dag once implemented


    def run(self):
        ''' Starts the interactive cli. Calls parser then handles input while running. '''
        print("\nWelcome to FriendNet! Please enter a command (type 'help' to see commands).\n")
        while self.running:
            raw = input("> ")
            command, args = self.parser.parse(raw)
            self.handle(command, args)


    def handle(self, command, args):
        ''' Check for command in the map. If present, retrieve value (method name in command.py)
        and call it, passing the graphs and args.'''
        try:
            if command in self.commands:
                func = COMMAND_MAP[command]
                if command == "help":
                    func(self.graphs, self.commands)
                elif command == "people":
                    func(self.graphs)
                elif command == "spread":
                    self.rumors.append(func(self.graphs, *args))
                else:
                    func(self.graphs, *args)
            else:
                logger.info(f"Unknown command: {command}")
        except Exception as e:
            logger.info(f"[Error] {e}")


