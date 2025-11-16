from .parser import Parser
from .commands import *

# Keys are commands, values are corresponding methods in commands.py
COMMAND_MAP = {
    "person": add_person,
    "people": print_people,
    "kill": remove_person,
    "connect": connect,
    "disconnect": disconnect,
    #"strengthen": strengthen_edge,
    #"weaken": weaken_edge,
    #"spread": spread_rumor
    "help": help_user
    
    # add more commands here
}

UNDIRECTED_COMMANDS = ["connect", "disconnect"]
DIRECTED_COMMANDS = []
WEIGHTED_COMMANDS = []
DAG_COMMANDS = []


class Interface:
    ''' CLI Interface '''
    def __init__(self, graphs: dict, parser: Parser):
        # Takes graph dict from cli.py to define which graph structures to use
        self.graphs = graphs
        self.parser = parser
        self.running = True
        #print("DEBUG", self.graphs)

        self.commands = {"help", "people", "person", "kill"}
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
                else:
                    func(self.graphs, *args)
            else:
                print(f"Unknown command: {command}")
        except Exception as e:
            print(f"[Error] {e}")


