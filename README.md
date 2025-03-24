# Hanabi AI

This project includes an implementation of the cooperative game Hanabi for one real player over the terminal and two AI players.

## 1. Getting Started
### Prerequisits
- Python 3.x
- Required libraries:
    - random
    - typing
    - numpy
    - enum

### Installation
Download all of the provided files and check, if your python environment meets all of the prerequisits listed above.
To run the program with a human player over the terminal, do:
```bash
python main.py
```
To run a test with just AI players over 500 games, do:
```bash
python main_AI_test.py
```
## 2. Overview
Our AI makes decision based on the probability matrix for each card, which stores the knowledge of the AI player of this card and calculates, how probabile it is for a card having a certain number and color and the state of the game.


## 3. Project Files
### main.py
This is the main entry point for the game. It initializes the players and the game state, and runs the game loop for one human player and two AI players.

### main_AI_test.py
This is the main entry point for a test. It initializes the players and the game state, and runs the game loop for three AI players.

### agent.py
This file contains the Agent class, which represents a player in the game. It includes methods for drawing, discarding, playing cards, and giving hints.

### state.py
This file contains the State class, which represents the game state. It includes methods for generating the deck, initializing playable cards, and updating probability matrices.

### evaluation.py
This file contains functions for evaluating the best actions for AI players, including playing, discarding, and giving hints.

### utils.py
This file contains utility functions for generating the deck, initializing playable cards, and checking if the game is over.
