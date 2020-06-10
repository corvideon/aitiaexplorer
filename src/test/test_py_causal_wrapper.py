import os

from tests.unit import TestAPI
import pandas as pd
from app.py_causal_wrapper import PyCausalWrapper
from pycausal import search as s
from pycausal.pycausal import pycausal


class Test_PyCausalWrapper(TestAPI):
    """
    TBD
    """
    wrapper = PyCausalWrapper()

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'resources/data')

    def tearDown(self):
        pass

    def test_get_tetrad(self):
        self.wrapper.start_vm()
        tetrad = self.wrapper.get_tetrad()
        self.wrapper.stop_vm()
        self.assertTrue(tetrad is not None)


    def test_get_algos(self):
        causal_discovery_algos = []
        for algo in self.wrapper.get_causal_discovery_algos():
            causal_discovery_algos.append(algo)
        self.assertTrue(len(causal_discovery_algos) == 25)


    def test_algo_bayes_est(self):
        data_dir = os.path.join(self.data_dir, "sim_discrete_data_20vars_100cases.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str = self.wrapper.algo_bayes_est(df)
        self.assertTrue(dot_str is not None, "No graph returned.")

    def test_algo_fges_continuous(self):
        data_dir = os.path.join(self.data_dir, "charity.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str = self.wrapper.algo_fges_continuous(df)
        self.assertTrue(dot_str is not None, "No graph returned.")

    def test_algo_fges_discrete(self):
        data_dir = os.path.join(self.data_dir, "audiology.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str = self.wrapper.algo_fges_discrete(df)
        self.assertTrue(dot_str is not None, "No graph returned.")

    def test_multiple_algo_run(self):
        dot_str_list = []

        pc = pycausal()
        pc.start_vm()
        tetrad = s.tetradrunner()

        data_dir = os.path.join(self.data_dir, "sim_discrete_data_20vars_100cases.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str_list.append(self.wrapper.algo_bayes_est(df, pc))

        data_dir = os.path.join(self.data_dir, "charity.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str_list.append(self.wrapper.algo_fges_continuous(df, pc))

        data_dir = os.path.join(self.data_dir, "audiology.txt")
        df = pd.read_table(data_dir, sep="\t")
        dot_str_list.append(self.wrapper.algo_fges_discrete(df, pc))

        pc.stop_vm()

        self.assertTrue(len(dot_str_list) == 3)

