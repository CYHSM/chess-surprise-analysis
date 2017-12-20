"""
Example code for evaluating a game and finding surprising moves
"""
from csa import csa

# Load Game from PGN
path_to_pgn = './games/alphazero-vs-stockfish_game2.pgn'
chess_game = csa.load_game_from_pgn(path_to_pgn)

# Evaluate Game
depths = range(1, 41)
cp, nodes = csa.evaluate_game(chess_game, reset_engine=True,
                              halfmove_numbers=None, depths=depths,
                              verbose=1, async_callback=True)
# Save cp
csa.save_evaluation(cp, nodes, depths, True,
                    True, 'alphazero_stockfish_game2')

# Plot heatmap
csa.plot_cp(cp, fn='alphazero_stockfish_game2.svg', save=True)

# Find surprising moves
ss_df, infos = csa.analyse_evaluations(cp, low=12, high=22)
