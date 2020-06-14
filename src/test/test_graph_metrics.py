import os

from tests.unit import TestAPI

from aitia_explorer.metrics.graph_metrics import GraphMetrics
from aitia_explorer.py_causal_wrapper import PyCausalWrapper
from aitia_explorer.util.graph_util import GraphUtil
from aitia_explorer.target_data.loader import TargetData


class Test_Metrics(TestAPI):
    """
    Tests for graph metrics.
    """
    wrapper = PyCausalWrapper()

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'resources/data')

    def tearDown(self):
        pass

    def test_load_simulated_data_graph(self):
        simulated_data = TargetData.simulated_data_1()
        self.assertTrue(simulated_data is not None, "No simulated data loaded.")

        graph = TargetData.simulated_data_1_graph()
        self.assertTrue(graph.edges() is not None, "No simulated data loaded.")
        self.assertTrue(graph.nodes() is not None, "No simulated data loaded.")

    def test_create_known_graph(self):
        graph = TargetData.simulated_data_1_graph()
        self.assertTrue(graph.edges() is not None, "No known simulated graph created.")
        self.assertTrue(graph.nodes() is not None, "No known simulated graph created.")

    def test_retrieve_adjacency_matrix(self):
        graph = TargetData.simulated_data_1_graph()
        metrics = GraphMetrics()
        adj_matrix = metrics.retrieve_adjacency_matrix(graph)
        self.assertTrue(adj_matrix is not None, "No adjacency matrix created.")

    def test_precision_recall(self):
        # get the simulated data
        simulated_data = TargetData.simulated_data_1()
        dot_str = self.wrapper.algo_pc(simulated_data)
        pred_graph = GraphUtil.get_digraph_from_dot(dot_str)

        # get the known data
        target_graph = TargetData.simulated_data_1_graph()
        metrics = GraphMetrics()
        prec_recall = metrics.precision_recall(target_graph, pred_graph)

        self.assertTrue(prec_recall[0] == 0.72)

    def test_precision_recall(self):
        # get the simulated data
        simulated_data = TargetData.simulated_data_1()
        dot_str = self.wrapper.algo_pc(simulated_data)
        pred_graph = GraphUtil.get_digraph_from_dot(dot_str)

        # get the known data
        target_graph = TargetData.simulated_data_1_graph()
        metrics = GraphMetrics()
        shd = metrics.SHD(target_graph, pred_graph)

        self.assertTrue(shd == 14)
