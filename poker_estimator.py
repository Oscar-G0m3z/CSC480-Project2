import random
import math
import sys
from collections import Counter

SUITS = ['s', 'h', 'd', 'c']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
FULL_DECK = [r + s for r in RANKS for s in SUITS]

# ------------------- Basic Hand Evaluator -------------------

def hand_strength(cards):
    assert len(cards) == 7
    rank_counts = Counter(c[0] for c in cards)
    max_count = max(rank_counts.values())
    return 1 if max_count >= 2 else 0

def evaluate_showdown(known_cards):
    hero = known_cards[:2]
    villain = known_cards[2:4]
    board = known_cards[4:]
    
    hero_strength = hand_strength(hero + board)
    villain_strength = hand_strength(villain + board)

    if hero_strength > villain_strength:
        return 1
    elif hero_strength == villain_strength:
        return 0.5
    else:
        return 0

# --------------------------------------

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state  # list of known cards
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def ucb1(self, child, c=math.sqrt(2)):
        if child.visits == 0:
            return float('inf')
        return (child.wins / child.visits) + c * math.sqrt(math.log(self.visits) / child.visits)

    def best_child(self):
        return max(self.children, key=lambda child: self.ucb1(child))

# --------------------------------------

def draw_random(deck, n):
    return random.sample(deck, n)

def expand_node(node):
    depth = len(node.state)
    deck = [card for card in FULL_DECK if card not in node.state]

    if depth == 2:  # Root: add opponent's hole cards
        samples = [draw_random(deck, 2) for _ in range(10)]
    elif depth == 4:  # Add flop
        samples = [draw_random(deck, 3) for _ in range(10)]
    elif depth == 7:  # Add turn
        samples = [draw_random(deck, 1) for _ in range(10)]
    elif depth == 8:  # Add river
        samples = [draw_random(deck, 1) for _ in range(10)]
    else:
        return  # Do not expand beyond river

    for new_cards in samples:
        child_state = node.state + new_cards
        child = MCTSNode(state=child_state, parent=node)
        node.children.append(child)

# --------------------------------------

def mcts_search(hole_cards, simulations=1000):
    root = MCTSNode(state=hole_cards)

    for _ in range(simulations):
        node = root
        path = [node]

        # Selection
        while node.children:
            node = node.best_child()
            path.append(node)

        # Expansion
        if len(node.state) < 9:
            expand_node(node)

        # Simulation
        if node.children:
            node = random.choice(node.children)
            path.append(node)

        full_state = node.state
        if len(full_state) < 9:
            remaining = 9 - len(full_state)
            deck = [card for card in FULL_DECK if card not in full_state]
            full_state += draw_random(deck, remaining)

        result = evaluate_showdown(full_state)

        # Backpropagation
        for n in path:
            n.visits += 1
            n.wins += result

    return root.wins / root.visits

# --------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python poker_estimator.py <card1> <card2> [simulations]")
        print("Example: python poker_estimator.py As Kh 2000")
        sys.exit(1)

    my_cards = [sys.argv[1], sys.argv[2]]
    simulations = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

    for card in my_cards:
        if card not in FULL_DECK:
            print(f"Invalid card: {card}")
            sys.exit(1)

    probability = mcts_search(my_cards, simulations=simulations)
    print(f"Estimated win probability for {my_cards}: {probability:.2%}")
