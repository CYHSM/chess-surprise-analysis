from python3.csa import csa
import matplotlib.pyplot as plt
import numpy as np
import importlib
import pickle
import os
import pandas as pd
import time
importlib.reload(csa)

# Load functions for saving / loading of evaluations
base_dir = '/home/marx/Documents/Programming/python/python3/csa/games/testgames/saved_analysis/'
def save_obj(obj, name):
    with open(base_dir + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(base_dir + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Load Game and Evaluate
path_to_pgn = '/home/marx/Documents/Programming/python/python3/csa/games/testgames/wei_yi_bruzon_batista_2015.pgn'
chess_game = csa.load_game_from_pgn(path_to_pgn)

t = time.time()
cp, nodes = csa.evaluate_game(chess_game, bln_reset_engine=True, halfmove_numbers=None, depths=range(1, 12), verbose=1, async_callback=True)
elapsed = time.time() - t
print(elapsed)

# Save cp and nodes
save_obj(cp, 'weiyi_cp')
save_obj(nodes, 'weiyi_nodes')
