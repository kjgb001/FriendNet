from .parser import Parser
from .commands import *
from view.controlPanel import ControlPanel
from view.matplotlibVisualizer import MatplotlibVisualizer

import logging
import traceback
import time
import sys
import select
import threading
import utils.logger as logger_mod

from PySide6.QtCore import QObject, Signal, Slot

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
    "rumors": print_rumors,

    "view": change_view,

    "start": start_sim,
    "stop": stop_sim,
    "tick": sim_tick,
    "speed": set_sim_speed,

    #"sim_init": sim_init, # TODO: Complete this command for the startup GUI to use
    
    # add more commands
}

UNDIRECTED_COMMANDS = ["connect", "disconnect"]
DIRECTED_COMMANDS = ["spread", "rumors"]
WEIGHTED_COMMANDS = ["strengthen", "weaken", "trust", "distrust"]
# DAG_COMMANDS = []
VIEW_COMMANDS = ["person", "kill", "reload", "connect", "disconnect",
                 "strengthen", "weaken", "spread", "view", "trust", "distrust"] # Which commands require a view redraw

class Interface(QObject):
    ''' CLI Interface '''

    command_requested = Signal(str, object)
    view_changed = Signal(str)
    rumor_selected = Signal(object)
    rumor_added = Signal()

    def __init__(self, parser: Parser):
        super().__init__()
        self.parser = parser
        self.running = True
        self.sim = None
        self.view = None
        self.suppress_view = False
        self.redraw_pending = False
        self.prompt_shown = False

        self.commands = {"help", "people", "person", "kill", "generate", 
                        "reload", "view", "rumors", "start", "stop", "tick",
                        "speed"}

        self.command_requested.connect(self._handle_on_main_thread)
        

    def view_init(self, simulation):
        self.view = MatplotlibVisualizer(simulation)

        self.controls = ControlPanel(self)
        self.controls.show()

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
        
        def input_loop():
            while self.running:
                # Show prompt once per input cycle
                if not self.prompt_shown:
                    print("> ", end="", flush=True)
                    self.prompt_shown = True

                ready, _, _ = select.select([sys.stdin], [], [], 0.1)

                if ready:
                    line = sys.stdin.readline()
                    if not line:
                        break  # EOF

                    command, args = self.parser.parse(line)
                    #print("EMITTING COMMAND") # DEBUG
                    self.command_requested.emit(command, args)

        # Start input thread
        threading.Thread(target=input_loop, daemon=True).start()

        # MAIN THREAD: redraw pump
        try:
            while self.running:
                if self.redraw_pending:
                    self.view.redraw()
                    self.redraw_pending = False

                self.view.pump_events(0.01)

        except KeyboardInterrupt:
            logger.info("Shutting down FriendNet...\n")
            self.running = False
            self.shutdown()


    def shutdown(self):
        if not self.running:
            return

        logger.info("Visualization closed. Shutting down FriendNet...\n")
        self.running = False

        # Stop simulation thread if running
        try:
            if self.sim:
                self.sim.stop()
        except:
            pass

        # Close control panel
        try:
            if self.controls:
                self.controls.close()
        except Exception:
            pass

        # Close view defensively
        try:
            self.view.close()
        except Exception:
            pass

        # Exit input thread
        try:
            sys.stdin.close()
        except Exception:
            pass


    @Slot(str, object)
    def _handle_on_main_thread(self, command, args):
        #print("RECEIVED COMMAND") # DEBUG
        self.handle(command, args, source="cli")

    def handle(self, command, args=None, source="sim"):
        """
        Execute a command that mutates simulation state.
        """
        #print(f"[DEBUG] suppress={logger_mod.suppress_commands}, cmd={command}") # DEBUG
        try:
            if command not in self.commands:
                logger.info(f"Unknown command: {command}")
                return

            func = COMMAND_MAP[command]

            # Command dispatch
            if command in ("start", "stop", "tick"):
                func(self.sim)

            elif command == "speed":
                func(self.sim, *(args or []))

            elif command == "help":
                func(self.sim.graphs, self.commands, *(args or []))

            elif command == "people":
                func(self.sim.graphs)

            elif command == "spread":
                rumor = func(self, self.sim.graphs, *(args or []))
                if not rumor:
                    return # Prevent edgeless rumors from persisting
                self.sim.rumors.append(rumor)
                self.view.set_rumor(rumor)
                self.rumor_added.emit()

            elif command == "rumors":
                func(self.sim.rumors)

            elif command == "reload":
                func(self)

            elif command == "generate":
                func(self, *(args or []))

            elif command == "view":
                success = func(self, self.sim.graphs, *(args or []))
                if success:
                    self.view_changed.emit(args[0])

            else:
                func(self, self.sim.graphs, *(args or []))

            # Signal redraw if this command affects the view
            if command in VIEW_COMMANDS:
                self.redraw_pending = True

        except Exception as e:
            logger.info(f"[Error] {e}")
            #traceback.print_exc()  # DEBUG
        
        finally:
            if source == "cli":
                self.prompt_shown = False

    def select_rumor(self, rumor):
        if rumor is None:
            return
        self.view.set_rumor(rumor)
        self.rumor_selected.emit(rumor)

    def suppress_output(self):
        logger_mod.suppress_commands = True
        self.suppress_view = True
    
    def resume_output(self):
        logger_mod.suppress_commands = False
        self.suppress_view = False


