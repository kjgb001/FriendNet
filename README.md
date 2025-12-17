# FriendNet

**A social simulation for learning graph theory built in Python.**

FriendNet turns classic graph structures into an interactive world where friendships and rumors play out as live data structures.  

*Note: This project is incomplete. Live simulation logic is not currently implemented.

---

## Overview

FriendNet is a progressive lab series that teaches students how different graph types behave in real systems, based on bespoke graph structures modified to act as scaffolding for students' own implementation logic.

Each lab builds on the last:
1. **Directed Graph** — Gossip and one sided relationships
2. **Undirected Graph** — Friendship web
3. **Weighted Graphs** — Trust and relationship strength

The simulation responds in real time to CLI commands like:  
connect Alice Bob
spread_rumor Alice
strengthen Alice Bob 1

(CLI is primitive and will be superceded by a GUI that calls commands via the interface)

A visualization window dynamically updates the social network as gossip spreads and relationships form, strengthen, or decay.

---

## Pedagogical Goals

- Reinforce understanding of **graph theory** through direct implementation.  
- Connect abstract data structures to real-world systems.  
- Encourage experimentation and debugging intuition through live feedback.

---

## Technical Stack

- **Python 3.11+**
- **unittest** — student testing  
- **networkx + matplotlib** — visualization  
- **logging** — event tracking  
- **argparse/cmd** — command parsing

---

## Setup & Run

Clone the repo:
```bash
git clone https://github.com/kjgb001/FriendNet.git
cd FriendNet
```

Run the simulation:
```bash
python run.py
```

Run tests:
```bash
pytest
```

## Developer Notes

- Visualization modules are pluggable — you can swap MatplotlibVisualizer for a new visualizer.

- Logging replaces all print statements for professional debugging.

- The FriendNet/student subdirectory is the student facing version, ready for use in the classroom.

# License

MIT License © 2025 Kellan Guinn-Bailey  
See [License](LICENSE) for details.

# Attribution

Designed as a TA project and pedagogical tool for the **CSCI 204: Data Structures** course at **Bucknell University** under the guidance of the Computer Science Department.

FriendNet is intended as an open educational tool for teaching graph theory, data structures, and experimental simulation design.
