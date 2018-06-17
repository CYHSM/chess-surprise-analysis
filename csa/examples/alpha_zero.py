"""
Run the analysis on all alpha zero games and save the resulting plot
"""
from csa import csa

# Load Game from PGN
for game_id in range(1, 11):
    path_to_pgn = './games/alphazero/alphazero-vs-stockfish_game{}.pgn'.format(game_id)
    chess_game = csa.load_game_from_pgn(path_to_pgn)

    # Evaluate Game
    depths = range(1, 35)
    cp, nodes = csa.evaluate_game(chess_game, reset_engine=True,
                                  halfmove_numbers=None, depths=depths,
                                  verbose=1, async_callback=True)
    # Save cp
    csa.save_evaluation(cp, nodes, depths, True,
                        True, 'alphazero_stockfish_game{}'.format(game_id))

    # Plot heatmap
    csa.plot_cp(cp, fn='alphazero/alphazero_stockfish_game{}.svg'.format(game_id), save=True)
