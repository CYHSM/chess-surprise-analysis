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
cp2 = cp.copy()
cp2[np.isnan(cp2)] = 0
plt.pcolor(cp2)

# In bokeh
from bokeh.plotting import figure, show, output_notebook
from bokeh.charts import HeatMap
#output_notebook()
import bokeh.palettes
p = HeatMap(cp2,x='move',y='depth')
# p = HeatMap(cp, title='csa', palette=bokeh.palettes.OrRd9)
show(p)

p2 = figure()
p2.line(ss_df)
show(p2)
import seaborn as sns
# sns.heatmap(cp_na.ix[:,46:48], cbar=False,
#                 square=False,
#                 annot=True,
#                 cmap='Blues',
#                 fmt='g',
#                 linewidths=0.5)
cp_na2 = cp_na.copy()
cp_na2[np.abs(cp_na2)>200] = 200
sns.heatmap(cp_na2)
sns.violinplot(cp_na.ix[:,45:50])
cp_na.ix[:,46:47]
cp_na = cp.fillna(method='pad')
cp_na = cp_na.fillna(method='bfill')
cp_na

ss_df = csa.analyse_evaluations(cp_na, low=12, high=22)
plt.plot(ss_df)
ss_df[abs(ss_df)>100]
ss_df[40::]

cp.ix[:,60::]
cp2 = cp
cp2[cp2>300] = 300
cp2[cp2<-300] = -300
cp2.ix[:,46::]
ss_cp2 = csa.analyse_evaluations(cp, low=12, high=20, end=30)
plt.plot(ss_cp2.diff())
# cp
plt.plot(ss_cp2)
ss_cp2[40::]
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
import pandas as pd

from bokeh.charts import HeatMap, bins, output_file, show
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
from bokeh.sampledata.autompg import autompg
from bokeh.sampledata.unemployment1948 import data

# setup data sources
#del data['Annual']
data['Year'] = data['Year'].astype(str)
unempl = pd.melt(data, var_name='Month', value_name='Unemployment', id_vars=['Year'])

hm10 = HeatMap(unempl, x='Year', y='Month', values='Unemployment', stat=None,
              sort_dim={'x': False}, width=900, plot_height=500)

output_file("heatmap.html", title="heatmap.py example")

show(hm10)

data
cp2[2]
cp2_melt = pd.melt(cp2, var_name='Moves', value_name='Evaluation', id_vars=[1:10])
cp2
cp4 = cp2.set_index(cp2[cp2.index[0]].astype(str))
cp4
cp3 = cp2.rename_axis('Depth')
HeatMap(cp2.values)
cp2

from bokeh._legacy_charts import HeatMap, output_file, show

xyvalues = np.random.random((28,1000))

df = pd.DataFrame(xyvalues)

output_file('heatmap.html')

plt.pcolor(cp2)

show(hm)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv')

data = [go.Heatmap( z=cp2.values.tolist(), colorscale='Viridis')]

plot(data, filename='pandas-heatmap')
