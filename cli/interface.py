from .parser import Parser
from .commands import *


COMMAND_MAP = {
    "person": add_person,
    "connect": connect
    #"strengthen": strengthen_edge,
    #"weaken": weaken_edge,
    #"spread": spread_rumor
    
    # add more commands here
}

class Interface:
    def __init__(self, graphs: dict, parser: Parser):
        # Takes graph dict from cli.py to define which graph structures to use
        self.graphs = graphs
        self.parser = parser
        self.running = True


    def run(self):
        ''' Starts the interactive cli. Calls parser then handles input while running. '''
        while self.running:
            raw = input("> ")
            command, args = self.parser.parse(raw)
            self.handle(command, args)


    def handle(self, command, args):
        ''' Check for command in the map. If present, retrieve value (method name in command.py)
        and call it, passing the graphs and args.'''
        try:
            if command in COMMAND_MAP:
                COMMAND_MAP[command](self.graphs, *args)
            else:
                print(f"Unknown command: {command}")
        except Exception as e:
            print(f"[Error] {e}")

