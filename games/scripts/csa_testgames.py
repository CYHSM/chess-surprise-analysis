from python3.csa import csa
import matplotlib.pyplot as plt
import numpy as np
import importlib
import pickle
import os
import pandas as pd
import time
importlib.reload(csa)
%matplotlib inline
# Test
# max_depth = list(range(14, 19))
# low_depths = list(range(1, 8))
# depths = low_depths + max_depth

base_dir = '/home/marx/Documents/Programming/python/python3/csa/games/testgames/saved_analysis/'
def save_obj(obj, name):
    with open(base_dir + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(base_dir + name + '.pkl', 'rb') as f:
        return pickle.load(f)


#path_to_pgn = '/home/marx/Documents/Programming/python/python3/csa/games/testgames/wei_yi_bruzon_batista_2015.pgn'
path_to_pgn = '/home/marx/Documents/Programming/python/python3/csa/games/testgames/kasparov_topalov_1999.pgn'
chess_game = csa.load_game_from_pgn(path_to_pgn)
# board = csa.get_board_at_position(chess_game, 13)
# board
# engine = csa.load_engine()
# cp = csa.evaluate_board(board, engine, depths=range(1, 11), verbose=1)
t = time.time()
cp, nodes = csa.evaluate_game(chess_game, bln_reset_engine=True, halfmove_numbers=None, depths=range(1, 33), verbose=1, async_callback=True)
elapsed = time.time() - t
print(elapsed)
save_obj(cp, 'kasparov_cp')
save_obj(nodes, 'kasparov_nodes')
# #
ss_df = csa.analyse_evaluations(cp, low=12, high=22)
low = 12
high = 22
low_mean = np.array(cp[low:high].mean())
high_mean = np.array(cp[high + 1::].mean())
c = pd.DataFrame(np.ma.log(low_mean).data)
d = pd.DataFrame(np.ma.log(high_mean).data)
c
ss_df = c-d
plt.plot(ss_df)
ss_df[abs(ss_df)>100]
ss_df[40::]

cp.ix[:,60::]
cp2 = cp
cp2[cp2>300] = 300
cp2[cp2<-300] = -300
cp2.ix[:,46::]
ss_cp2 = csa.analyse_evaluations(cp2, low=12, high=20)
plt.plot(ss_cp2)
# cp
#
cp = load_obj('kasparov_cp')
cp.ix[:,45::]
# # cp.ix[:,45::]
# plt.pcolor(cp.ix[:,52:56])
# board_tmp = csa.get_board_at_position(chess_game, 48)
# board_tmp
# cp[48]
# list_values = [ v for v in cp[0].values()]
# list_values
# z_lv = (list_values - np.mean(list_values)) / np.std(list_values)
# plt.plot(list_values)
# plt.plot(z_lv)
#
# np.mean(list_values[12::])
# np.mean(list_values[5:11])
# np.std(list_values[5:11])
# surprise_factor = np.mean(list_values[0:11]) - np.mean(list_values[12::])
# surprise_factor

#---------------------------

# cp_per_move, nodes_per_move = csa.evaluate_game(chess_game, depths=depths)
#
# # Plot half moves
# cp_low_history = []
# cp_high_history = []
# for move in cp_per_move:
#     this_move = cp_per_move[move]
#     avg_cp_low = np.mean([this_move[depth] for depth in low_depths])
#     avg_cp_high = np.mean([this_move[depth] for depth in max_depth])
#     cp_low_history.append(avg_cp_low)
#     cp_high_history.append(avg_cp_high)
#     # print(avg_cp_low)
#
# max_diff = np.argmax(np.abs(cp_low_history) - np.abs(cp_high_history))
# cp_low_history_z = (cp_low_history - np.nanmean(cp_low_history)
#                     ) / np.nanstd(cp_low_history)
# cp_high_history_z = (
#     cp_high_history - np.nanmean(cp_high_history)) / np.nanstd(cp_high_history)
# plt.plot(cp_low_history)
# plt.plot(cp_high_history)
# #plt.plot((44, 44), (-800, 600), 'k-')
# plt.legend(['low', 'high'])
# plt.show()
