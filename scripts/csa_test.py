import chess.uci
import chess.pgn
import os
import matplotlib.pyplot as plt
import seaborn
from collections import defaultdict
import time
%matplotlib inline

# Test Stockfish engine
engine = chess.uci.popen_engine('stockfish')
engine.uci()
# With info handler to get scores
info_handler = chess.uci.InfoHandler()
engine.info_handlers.append(info_handler)

# Read Game
base_dir = os.getcwd()
pgn = open(base_dir + '/games/testgames/wei_yi_bruzon_batista_2015.pgn')
this_game_pgn = chess.pgn.read_game(pgn)
this_game = this_game_pgn

def evaluate_board(board, depth=10):
    """Evaluates a board and returns the centipawn evaluation"""
    engine.position(board)
    engine.go(depth=depth)
    centipawn_eval = info_handler.info['score'][1].cp
    if centipawn_eval is None:
        centipawn_eval = 0
    return centipawn_eval if board.turn else -1*centipawn_eval

# Iterate through moves
centipawn_history = defaultdict(list)
while not this_game.is_end():
    next_node = this_game.variation(0)
    next_board = next_node.board()
    this_centipawn_low = evaluate_board(next_board,depth=5)
    this_centipawn_high = evaluate_board(next_board,depth=10)
    centipawn_history['low'].append(this_centipawn_low)
    centipawn_history['high'].append(this_centipawn_high)
    this_game = next_node

plt.plot(centipawn_history['low'])
plt.plot(centipawn_history['high'])
plt.legend(['low', 'high'])
plt.show()

# Check continous evaluation
depth_history = {}
engine.position(next_board)
engine.go(depth=25, async_callback=True)
depth = 0
while depth != 25:
    if 1 in info_handler.info["score"]:
        centipawn_eval = info_handler.info["score"][1].cp
        print("Score: ", centipawn_eval)
        depth = info_handler.info["depth"]
        depth_history[depth] = centipawn_eval
        print("Depth: ", depth)

# Synchron with loop
depth_history = {}
nodes = {}
engine.position(next_board)
for i in range(25):
    engine.go(depth=i)
    centipawn_eval = info_handler.info["score"][1].cp
    depth = info_handler.info["depth"]
    print(depth==i)
    depth_history[i] = centipawn_eval
    nodes[i] = info_handler.info["nodes"]
print('Done')

plt.plot(depth_history)
