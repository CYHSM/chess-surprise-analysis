import os
import unittest
from csa import csa

import numpy as np


class TestCsa(unittest.TestCase):
    """Simple Testing Class"""

    def setUp(self):
        """Set up a chess game"""
        unittest.TestCase.setUp(self)

        # Load Game from PGN
        base_dir = os.path.dirname(__file__) + '/test_files/'
        path_to_pgn = base_dir + 'kasparov_topalov_1999.pgn'
        chess_game = csa.load_game_from_pgn(path_to_pgn)

        # Save for other test methods
        self.chess_game = chess_game

    def test_asynchrone_evaluation(self):
        """
        Tests asynchrone evaluation
        """
        # Evaluate Game / Check here None in halfmove_numbers
        cp, nodes = csa.evaluate_game(self.chess_game, reset_engine=True,
                                      halfmove_numbers=None, depths=range(1, 3),
                                      verbose=0, async_callback=True)

    def test_synchrone_evaluation(self):
        """
        Tests asynchrone evaluation
        """
        # Evaluate Game
        cp, nodes = csa.evaluate_game(self.chess_game, reset_engine=True,
                                      halfmove_numbers=[1, 2, 3], depths=range(1, 3),
                                      verbose=0, async_callback=False)

    def test_analyse_evaluations(self):
        """
        Tests if cp can be analysed to return surprising moves
        """
        import pandas as pd
        cp = pd.DataFrame([[1,2,3,4],[3,4,5,6],[5,4,5,6],[3,6,2,1]])
        ss_df, infos = csa.analyse_evaluations(cp, low=1, high=2)

    def test_save_and_load(self):
        """
        Tests if evaluations can be saved/loaded (pickled)
        """
        # Save evaluations and infos
        cp_in = [1, 2, 3]
        nodes_in = [4, 5, 6]
        depths_in = range(1, 5)
        async_callback_in = False
        reset_engine_in = True
        name = '2016_markus_jannis'

        csa.save_evaluation(cp_in, nodes_in, depths=depths_in,
                            async_callback=async_callback_in,
                            reset_engine=reset_engine_in,
                            name=name)

        # Travis does not allow save so return if file not there
        return
        # Load again
        cp, nodes, depths, async_callback, reset_engine = csa.load_evaluation(
            name)

        self.assertEqual(cp_in, cp)
        self.assertEqual(nodes_in, nodes)
        self.assertEqual(depths_in, depths)
        self.assertEqual(async_callback_in, async_callback)
        self.assertEqual(reset_engine_in, reset_engine)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
