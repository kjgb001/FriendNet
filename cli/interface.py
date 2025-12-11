from .parser import Parser
from .commands import *
from view.matplotlibVisualizer import MatplotlibVisualizer

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

    "view": change_view
    
    # add more commands
}

UNDIRECTED_COMMANDS = ["connect", "disconnect"]
DIRECTED_COMMANDS = ["spread"]
WEIGHTED_COMMANDS = ["strengthen", "weaken", "trust", "distrust"]
# DAG_COMMANDS = []
VIEW_COMMANDS = ["person", "kill", "reload", "connect", "disconnect",
                 "strengthen", "weaken", "spread", "view"] # Which commands require a view redraw

class Interface:
    ''' CLI Interface '''
    def __init__(self, parser: Parser):
        self.parser = parser
        self.running = True
        self.sim = None
        self.view = None
        self.suppress_view = False

        self.commands = {"help", "people", "person", "kill", "generate", "reload", "view"}
        

    def view_init(self, simulation):
        self.view = MatplotlibVisualizer(simulation)

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
        logger.info("\nWelcome to FriendNet! Please enter a command (type 'help' to see commands).\n")
        
        try:
            while self.running:
                raw = input("> ")
                command, args = self.parser.parse(raw)
                self.handle(command, args)
        except KeyboardInterrupt:
            logger.info("Shutting down FriendNet...")
            self.view.close()
            raise


    def handle(self, command, args = None):
        ''' Check for command in the map. If present, retrieve value (method name in command.py)
        and call it, passing the graphs and args.'''
        
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

            if command in VIEW_COMMANDS and not self.suppress_view:
                rumor = self.sim.rumors[-1]
                self.view.redraw(self.sim, rumor)

        except Exception as e:
            logger.info(f"[Error] {e}")
            traceback.print_exc() # DEBUG


    def suppress_output(self):
        logger_mod.suppress_commands = True
        self.suppress_view = True
    
    def resume_output(self):
        logger_mod.suppress_commands = False
        self.suppress_view = False


