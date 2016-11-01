"""
csa : Chess Surprise analysis
author : Markus Frey
e-mail : markus.frey1@gmail.com
"""
import chess.pgn
import chess.uci
import numpy as np
import pandas as pd


def load_engine():
    """Load engine for analysing games"""
    # Use the open-soure engine Stockfish
    engine = chess.uci.popen_engine('stockfish')
    # Important to use UCI (Universal Chess Interface)
    engine.uci()
    # Use an InfoHandler to save information about the analysis
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)

    return engine


def reset_engine(engine):
    """Reset the engine to avoid usage of hashtables in evaluation.

    Problem: After first analysis a lot of possible moves are stored in
        the hashtable so a re-run on low depths will lead to evaluations
        based on higher depths

    """
    engine.quit()
    engine = load_engine()
    return engine


def load_game_from_pgn(path_to_pgn):
    """Read a chess game from PGN"""
    # Open PGN
    pgn = open(path_to_pgn)
    # Read game information
    chess_game = chess.pgn.read_game(pgn)

    return chess_game


def get_board_at_position(chess_game, position):
    """
    Given a chess game, returns the board at given position
    """
    fullmove_number = chess_game.board().fullmove_number
    while not chess_game.is_end() and fullmove_number - 1 < position:
        board = chess_game.board()
        next_node = chess_game.variation(0)
        chess_game = next_node
        fullmove_number = chess_game.board().fullmove_number
    return board


def evaluate_game(chess_game, move_numbers=None, bln_reset_engine=True,
                  depths=range(5, 20), verbose=0):
    """
    Evaluate each move of the game

    Inputs:
    - chess_game : The game to analyse
    - move_numbers : Specify the move numbers which should be analysed,
                    None analyses all
    - bln_reset_engine : Boolean if engine should be reset during moves,
                        otherwise will lead to different results due to hashing
    - depths : Specify the depths which should be analysed
    - verbose : Specify if output should be printed (0,1)

    Outputs:
    - cp_per_move : Centipawn evaluation over all depths per move
    - nodes_per_move : How many nodes were evaluated over all depths per move

    """
    # Initialise Outputs
    cp_per_move = {}
    nodes_per_move = {}
    halfmove_counter = 1
    # Get engine
    engine = load_engine()
    # Loop over all moves
    while not chess_game.is_end():
        board = chess_game.board()
        next_node = chess_game.variation(0)
        chess_game = next_node
        if move_numbers is not None:
            if halfmove_counter not in move_numbers:
                halfmove_counter += 1
                continue
        # Reset engine
        if bln_reset_engine:
            engine = reset_engine(engine)
        # Evaluate board
        if verbose:
            print('Evaluating half-move %d, Depth: ' % halfmove_counter, end='')
        cp_per_depth, nodes_per_depth = evaluate_board(
            board, engine, depths=depths, verbose=verbose)
        # Save Outputs
        cp_per_move[halfmove_counter] = cp_per_depth
        nodes_per_move[halfmove_counter] = nodes_per_depth
        halfmove_counter += 1
        if verbose:
            print('')
    # Return as dataframe
    cp_per_move = pd.DataFrame.from_dict(cp_per_move)
    nodes_per_move = pd.DataFrame.from_dict(cp_per_move)
    return cp_per_move, nodes_per_move


def evaluate_board(board, engine, depths=range(5, 20), verbose=0):
    """
    Evaluates the current position on the board

    Inputs:
    - board: Contains all the information about the position of the pieces
    - engine: Engine used to evaluate Position

    Outputs:
    - cp_per_depth: Centipawn Evaluation per depth used
    - nodes_per_depth: How many nodes where evaluated at this depth
    """
    # Initialise Outputs
    cp_per_depth = {}
    nodes_per_depth = {}
    # Set board position
    engine.position(board)
    for depth in depths:
        if verbose:
            print('%d,' % depth, end='')
        engine.go(depth=depth)  # Run analysis
        centipawn_eval = engine.info_handlers[0].info[
            "score"][1].cp  # Get evaluation from info_handler
        # Catch problems with the evaluation
        if centipawn_eval is None:
            centipawn_eval = np.NaN
        # Make sure the evaluation is not dependent on the side to move
        if not board.turn:
            centipawn_eval *= -1
        cp_per_depth[depth] = centipawn_eval
        nodes_per_depth[depth] = engine.info_handlers[0].info["nodes"]
    return cp_per_depth, nodes_per_depth


def analyse_evaluations(cp_df, low=5, high=11):
    """
    Analyses evaluations and returns 'surprise' scores

    Inputs:
    - cp_df : Dataframe of evaluations in centipawns.
            Dimensions: #Depths x #Moves
    - low : Human range of chess ;)
    - high : Computer range ;)

    Outputs:
    - ss_df : Dataframe with surprise scores. Dimension: #Moves
    """
    low_mean = cp_df[low:high].mean()
    high_mean = cp_df[high+1::].mean()
    ss_df = low_mean - high_mean

    return ss_df
