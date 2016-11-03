"""
Example code for evaluating a game and finding surprising moves
"""
import csa

# Load Game from PGN
path_to_pgn = 'wei_yi_bruzon_batista_2015.pgn'
chess_game = csa.load_game_from_pgn(path_to_pgn)

# Evaluate Game
cp, nodes = csa.evaluate_game(chess_game, bln_reset_engine=True,
                              halfmove_numbers=None, depths=range(1, 35),
                              verbose=1, async_callback=True)

# Find surprising moves
ss_df, infos = csa.analyse_evaluations(cp, low=12, high=22)
