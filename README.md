# CSC480-Project2
Poker I hardly know her

## Features

- Layered MCTS tree structure: opponent → flop → turn → river
- Basic hand evaluator (pair vs. high card)
- Command-line interface

SUITS = ['s', 'h', 'd', 'c']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card = Rank + Suit

### Run the script
```bash
python3 poker_estimator.py <card1> <card2> [simulations]
EX : python3 poker_estimator.py As Js 1000