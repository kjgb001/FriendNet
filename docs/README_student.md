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
connect Alice Bob
spread_rumor Alice Bob "Bob smells like rancid milk"
strengthen Alice Bob 5

A visualization window dynamically updates with the social network as gossip spreads and relationships form, strengthen, decay, and dissolve.

---

## Python Version + External Liraries

- **Python 3.10 +**
- **networkx + matplotlib**: basic visualization 
- **PySide6**: Qt visualization backend, window engine, and signals

---

## How to Run

Install dependencies:
```bash
pip install networkx matplotlib PySide6 pytest
```

Run the simulation:
```bash
python run.py
```

# License

MIT License © 2025 Kellan Guinn-Bailey  
See [License](LICENSE) for details.

# Attribution

Designed as a TA project and pedagogical tool for the **Computer Science Department** at **Bucknell University**.  

FriendNet is intended as an open educational tool for teaching graph theory, data structures, and simulation design.
