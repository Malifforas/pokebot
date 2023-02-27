from .decision import *
from .action import *
from game_state import GameState
def choose_best_move(game_state):
    """
    Chooses the best move to perform in the current game state.

    Args:
        game_state (GameState): The current game state.

    Returns:
        Move: The best move to perform.
    """
    moves = game_state.get_possible_moves()
    best_move = None
    best_score = float('-inf')
    for move in moves:
        score = evaluate_move(move, game_state)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

def evaluate_move(move, game_state):
    """
    Evaluates the score of a given move in the current game state.

    Args:
        move (Move): The move to evaluate.
        game_state (GameState): The current game state.

    Returns:
        float: The score of the move.
    """
    action = get_action(move)
    score = action.get_score(game_state)
    decision = make_decision(move, game_state)
    score += decision.get_score(game_state)
    return score

def get_possible_outcomes(move, game_state):
    """
    Returns a list of possible game states that could result from performing a given move in the current game state.

    Args:
        move (Move): The move to perform.
        game_state (GameState): The current game state.

    Returns:
        list: A list of possible game states.
    """
    action = get_action(move)
    outcomes = action.get_possible_outcomes(game_state)
    return outcomes