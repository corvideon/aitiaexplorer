"""
TBD
"""
import logging
import os
import pandas as pd

_logger = logging.getLogger(__name__)


class TargetData:
    """
    A class that provides known causal data for targetting in tests.
    """

    def __init__(self):
        pass

    @staticmethod
    def data_dir():
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        return data_dir

    @staticmethod
    def graphs_dir():
        graphs_dir = os.path.join(os.path.dirname(__file__), 'graphs')
        return graphs_dir

    @staticmethod
    def simulated_data_1_graph():
        graph_path = os.path.join(TargetData.graphs_dir(), "simulated_data_graph_1.dot")
        with open(graph_path, 'r') as dot_file:
            simulated_data_graph = dot_file.read()
        return simulated_data_graph

    @staticmethod
    def simulated_data_1():
        data_dir = os.path.join(TargetData.data_dir(), "simulated_data_1.txt")
        simulated_data = pd.read_table(data_dir, sep="\t")
        return simulated_data

    @staticmethod
    def audiology_data():
        data_dir = os.path.join(TargetData.data_dir(), "audiology.txt")
        return pd.read_table(data_dir, sep="\t")

    @staticmethod
    def charity_data():
        data_dir = os.path.join(TargetData.data_dir(), "charity.txt")
        return pd.read_table(data_dir, sep="\t")

    @staticmethod
    def lucas0_data():
        """
        See http://www.causality.inf.ethz.ch/data/LUCAS.html
        :return:
        """
        data_dir = os.path.join(TargetData.data_dir(), "lucas0_train.csv")
        return pd.read_csv(data_dir)

    @staticmethod
    def lucas2_data():
        """
        See http://www.causality.inf.ethz.ch/data/LUCAS.html
        :return:
        """
        data_dir = os.path.join(TargetData.data_dir(), "lucas0_train.csv")
        return pd.read_csv(data_dir)