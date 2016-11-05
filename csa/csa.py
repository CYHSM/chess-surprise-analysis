"""
csa : Chess Surprise analysis
author : Markus Frey
e-mail : markus.frey1@gmail.com
github : https://github.com/CYHSM/chess-surprise-analysis
"""
import chess.pgn
import chess.uci
import numpy as np
import pandas as pd
import pickle
import os


###############################################################################
#####################LOAD GAME AND BOARD#######################################
###############################################################################
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


def reset_present_engine(engine):
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
    pgn_file = open(path_to_pgn)
    # Read game information
    chess_game = chess.pgn.read_game(pgn_file)
    # Close
    pgn_file.close()

    return chess_game


def get_board_at_position(chess_game, halfmove_number):
    """
    Given a chess game, returns the board at given halfmove_number
    """
    halfmove_counter = 1
    while not chess_game.is_end() and halfmove_counter - 1 < halfmove_number:
        board = chess_game.board()
        next_node = chess_game.variation(0)
        chess_game = next_node
        halfmove_counter += 1
    return board


###############################################################################
#####################GAME EVALUATION###########################################
###############################################################################
def evaluate_game(chess_game, halfmove_numbers=None, reset_engine=True,
                  depths=range(5, 20), verbose=0, async_callback=False,
                  fillna=True):
    """
    Evaluate each move of the game

    Inputs:
    - chess_game : The game to analyse
    - halfmove_numbers : Specify the move numbers which should be analysed,
                    None analyses all
    - reset_engine : Boolean if engine should be reset during moves,
                        otherwise will lead to different results due to hashing
    - depths : Specify the depths which should be analysed
    - verbose : Specify if output should be printed (0,1)
    - async_callback : Boolean if calculation should be performed asynchrone

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
        if halfmove_numbers is not None:
            if halfmove_counter not in halfmove_numbers:
                halfmove_counter += 1
                continue
        # Reset engine
        if reset_engine:
            engine = reset_present_engine(engine)
        # Evaluate board
        if verbose:
            print('Evaluating half-move %d, Depth: ' %
                  halfmove_counter, end='')
        if async_callback:
            cp_per_depth, nodes_per_depth = evaluate_board_asynchrone(
                board, engine, max_depth=np.max(depths), verbose=verbose)
        else:
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
    # Fill Nan Values as asynchrone evaluation skips depths
    if fillna:
        cp_per_move = cp_per_move.fillna(method='pad').fillna(method='bfill')
        nodes_per_move = nodes_per_move.fillna(method='pad').fillna(method='bfill')

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


def evaluate_board_asynchrone(board, engine, max_depth=20, verbose=0):
    """
    Evaluates the current position on the board in an asynchrone way

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
    current_depth = 1

    # Set board position
    engine.position(board)
    engine.go(depth=max_depth, async_callback=True)
    while current_depth != max_depth:
        if 1 in engine.info_handlers[0].info["score"]:
            centipawn_eval = engine.info_handlers[0].info[
                "score"][1].cp  # Get evaluation from info_handler
            # Catch problems with the evaluation
            if centipawn_eval is None:
                centipawn_eval = np.NaN
            # Make sure the evaluation is not dependent on the side to move
            if not board.turn:
                centipawn_eval *= -1
            if current_depth != engine.info_handlers[0].info["depth"]:
                current_depth = engine.info_handlers[0].info["depth"]
                if verbose:
                    print('%d,' % current_depth, end='')
            # Save values
            cp_per_depth[current_depth] = centipawn_eval
            if engine.info_handlers[0].info["nodes"]:
                nodes_per_depth[current_depth] = engine.info_handlers[
                    0].info["nodes"]
    engine.stop()
    return cp_per_depth, nodes_per_depth


def analyse_evaluations(cp_df, low=5, high=11, end=None, use_log=True):
    """
    Analyses evaluations and returns 'surprise' scores

    Inputs:
    - cp_df : Dataframe of evaluations in centipawns.
            Dimensions: #Depths x #Moves
    - low : Human range of chess ;)
    - high : Computer range ;)

    Outputs:
    - ss_df : Dataframe with surprise scores. Dimension: #Moves
    - infos : Dict with additional parameters
    """
    infos = {}
    low_mean = cp_df[low:high].mean()
    if end is not None:
        high_mean = cp_df[high + 1:end].mean()
    else:
        high_mean = cp_df[high + 1::].mean()
    if use_log:
        # Be aware of 0 division if using logarithmic identity : log(a/b) = log(a) - log(b)
        # Here we use masked numpy array to fix zero values
        low_log = np.ma.log(np.abs(low_mean.values)).data * np.sign(low_mean.values)
        high_log = np.ma.log(np.abs(high_mean.values)).data * np.sign(high_mean.values)
        ss_df = pd.DataFrame(low_log - high_log, index=cp_df.columns)
        infos['low_log'] = low_log
        infos['high_log'] = high_log
    else:
        ss_df = low_mean - high_mean
    infos['low_mean'] = low_mean
    infos['high_mean'] = high_mean

    return ss_df, infos


###############################################################################
#####################SAVE EVALUATIONS##########################################
###############################################################################
def save_evaluation(cp, nodes, depths, async_callback,
                    reset_engine, name):
    """
    Saves the evaluations with other information in a file

    Inputs:
    - cp : Dataframe of evaluations in centipawns.
            Dimensions: #Depths x #Moves
    - nodes : Dataframe of how many nodes were evaluated at which depth
    - depths : How far did the engine calculate
    - reset_engine : Boolean if engine was reset during moves,
                    otherwise will lead to different results due to hashing
    - async_callback : Boolean if calculation should be performed asynchrone
    - name : Specify as year_opponent1_opponent2
    """
    # Construct dict for saving
    obj = {}
    obj['cp'] = cp
    obj['nodes'] = nodes
    obj['depths'] = depths
    obj['async_callback'] = async_callback
    obj['reset_engine'] = reset_engine
    # Save to file
    base_dir = os.path.dirname(__file__)+'/evaluations/'
    with open(base_dir + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_evaluation(name):
    """
    Load the evaluations with other informations from file

    Inputs:
    - name : Name of file, in format year_opponent1_opponent2

    Outputs:
    - cp : Dataframe of evaluations in centipawns.
            Dimensions: #Depths x #Moves
    - nodes : Dataframe of how many nodes were evaluated at which depth
    - depths : How far did the engine calculate
    - reset_engine : Boolean if engine was reset during moves,
                    otherwise will lead to different results due to hashing
    - async_callback : Boolean if calculation should be performed asynchrone
    - name : Specify as year_opponent1_opponent2
    """
    # Load from file
    base_dir = os.path.dirname(__file__)+'/evaluations/'
    with open(base_dir + name + '.pkl', 'rb') as f:
        obj = pickle.load(f)
    cp = obj['cp']
    nodes = obj['nodes']
    depths = obj['depths']
    async_callback = obj['async_callback']
    reset_engine = obj['reset_engine']
    # Return
    return cp, nodes, depths, async_callback, reset_engine
