# FriendNet

**A social simulation for learning graph theory built in Python.**

FriendNet turns classic graph structures into an interactive GUI + command-line world where friendships and rumors play out as live data structures.  

---

## Overview

FriendNet is a progressive lab series that teaches students how different graph types behave in real systems, based on bespoke graph structures translated to act as scaffolding for students' own implementation logic.

Each lab builds on the last:
1. **Undirected Graph** — Friendship web
2. **Directed Graph** — Gossip
3. **Weighted Graphs** — Trust and relationship strength

The simulation responds in real time to CLI commands like:  
- connect Alice Bob  
- spread_rumor Alice Bob "Bob smells like rancid milk"  
- strengthen Alice Bob 5  

A visualization window dynamically updates with the social network as gossip spreads and relationships form, strengthen, decay, and dissolve.

---

## Pedagogical Goals

- Reinforce understanding of **graph theory** through direct implementation.  
- Build student comfort with **command-line interaction** (optional).  
- Connect abstract data structures to real systems.  
- Encourage experimentation and debugging intuition through live feedback.

---

## Python Version + External Liraries

- **Python 3.10 +**
- **pytest**: internal testing (not required for students)
- **networkx + matplotlib**: basic visualization 
- **PySide6**: Qt visualization backend, window engine, and signals

---

## Setup & Run

Clone the repo:
```bash
git clone https://github.com/kjgb001/FriendNet.git
cd FriendNet
```

Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Run the simulation:
```bash
python3 run.py
```

Run tests:
```bash
pytest
```

To generate a student-facing copy of FriendNet, run:
```bash
python3 build_student.py
```
The output will appear in the
"student/"
directory

## Developer Notes

- This currently has only been tested on Linux, but *should* be OS agnostic.

- pytest is used internally for autograding, but students write their own tests with unittest.

- Logging replaces print statements for better debugging and output control.

- Weights range from 1.0-2.0 inclusive to allow for 0 to represent a non-edge.

- Non-weighted graph add_vertex functions take a weight param defaulted to None for a consistent Abstract Base Class contract.

- The matrix based graph implementation present represents my personal learning process with writing bespoke graph structures (I know it's messy), and is not intended to be exposed to students. I recommend students implement adjacency *list* based graphs.

## Areas for Improvement

- Weight bounds are currently hard-coded into the application, could be an enumeration. Some other "magic numbers" should at least be constants as well.

- Simulation loop mutations could be improved and expanded upon.

- GUIs have lots of room for improvement, especially via added controls.

- People could have personality traits that impact friendship formation/mutation, trust, and rumor spreading logic.

- Rumor logic in general could be improved, mainly so that friendship level impacts the chance that they will propogate the rumor.

- Pygame based or other advanced visualization class could be added as an option, along with alternate vizualization themeing.

- A more advanced cli system could be implemented, current cli is very 'dumb'.

- Search algorithms could be added for graph analysis, alongside live data collection and visualization as the simulation runs.

- The simulation could be extended into a gaming experience by adding Directed Acyclic Graphs for quests, and allowing students to easily drop in a custom 'player' node. Save/Load states would enhance this further.

# License

MIT License © 2025 Kellan Guinn-Bailey  
See [License](LICENSE) for details.

# Attribution

Designed as a TA project and pedagogical tool for the **Computer Science Department** at **Bucknell University**.  

FriendNet is intended as an open educational tool for teaching graph theory, data structures, and simulation design.
