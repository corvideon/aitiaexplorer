"""
Based on code from https://github.com/FenTechSolutions/CausalDiscoveryToolbox/
which was originally released under an MIT License.
"""
import logging

import networkx as nx
import numpy as np
from sklearn.metrics import auc, precision_recall_curve

_logger = logging.getLogger(__name__)


class GraphMetrics:
    """
    A class for measuring differences between graphs.
    """

    def __init__(self):
        pass

    def retrieve_adjacency_matrix(self, graph, order_nodes=None, weight=False):
        """Retrieve the adjacency matrix from the nx.DiGraph or numpy array."""
        if isinstance(graph, np.ndarray):
            return graph
        elif isinstance(graph, nx.DiGraph):
            if order_nodes is None:
                order_nodes = graph.nodes()
            if not weight:
                return np.array(nx.adjacency_matrix(graph, order_nodes, weight=None).todense())
            else:
                return np.array(nx.adjacency_matrix(graph, order_nodes).todense())
        else:
            raise TypeError("Only networkx.DiGraph and np.ndarray (adjacency matrixes) are supported.")

    def precision_recall(self, target, prediction, low_confidence_undirected=False):
        r"""Compute precision-recall statistics for directed graphs.

        Precision recall statistics are useful to compare algorithms that make
        predictions with a confidence score. Using these statistics, performance
        of an algorithms given a set threshold (confidence score) can be
        approximated.
        Area under the precision-recall curve, as well as the coordinates of the
        precision recall curve are computed, using the scikit-learn library tools.
        Note that unlike the AUROC metric, this metric does not account for class
        imbalance.
        Precision is defined by: :math:`Pr=tp/(tp+fp)` and directly denotes the
        total classification accuracy given a confidence threshold. On the other
        hand, Recall is defined by: :math:`Re=tp/(tp+fn)` and denotes
        misclassification given a threshold.
        Args:
            target (numpy.ndarray or networkx.DiGraph): Target graph, must be of
                ones and zeros.
            prediction (numpy.ndarray or networkx.DiGraph): Prediction made by the
                algorithm to evaluate.
            low_confidence_undirected: Put the lowest confidence possible to
                undirected edges (edges that are symmetric in the confidence score).
                Default: False
        Returns:
            tuple: tuple containing:
                + Area under the precision recall curve (float)
                + Tuple of data points of the precision-recall curve used in the computation of the score (tuple).
        Examples:
            tar, pred = np.random.randint(2, size=(10, 10)), np.random.randn(10, 10)
            # adjacency matrixes of size 10x10
            aupr, curve = precision_recall(target, input)
            # leave low_confidence_undirected to False as the predictions are continuous
        """
        true_labels = self.retrieve_adjacency_matrix(target)
        pred = self.retrieve_adjacency_matrix(
            prediction,
            target.nodes()
            if isinstance(target, nx.DiGraph) else None,
            weight=True)

        if low_confidence_undirected:
            # Take account of undirected edges by putting them with low confidence
            pred[pred == pred.transpose()] *= min(min(pred[np.nonzero(pred)]) * .5, .1)
        precision, recall, _ = precision_recall_curve(true_labels.ravel(), pred.ravel())
        aupr = auc(recall, precision)

        return aupr, list(zip(precision, recall))

    def SHD(self, target, pred, double_for_anticausal=True):
        """Compute the Structural Hamming Distance.
        The Structural Hamming Distance (SHD) is a standard distance to compare
        graphs by their adjacency matrix. It consists in computing the difference
        between the two (binary) adjacency matrixes: every edge that is either
        missing or not in the target graph is counted as a mistake. Note that
        for directed graph, two mistakes can be counted as the edge in the wrong
        direction is false and the edge in the good direction is missing ; the
        `double_for_anticausal` argument accounts for this remark. Setting it to
        `False` will count this as a single mistake.
        Args:
            target (numpy.ndarray or networkx.DiGraph): Target graph, must be of
                ones and zeros.
            prediction (numpy.ndarray or networkx.DiGraph): Prediction made by the
                algorithm to evaluate.
            double_for_anticausal (bool): Count the badly oriented edges as two
                mistakes. Default: True

        Returns:
            int: Structural Hamming Distance (int).
                The value tends to zero as the graphs tend to be identical.
        Examples:
            from numpy.random import randint
            tar, pred = randint(2, size=(10, 10)), randint(2, size=(10, 10))
            SHD(tar, pred, double_for_anticausal=False)
        """
        true_labels = self.retrieve_adjacency_matrix(target)
        predictions = self.retrieve_adjacency_matrix(pred, target.nodes()
        if isinstance(target, nx.DiGraph) else None)

        diff = np.abs(true_labels - predictions)
        if double_for_anticausal:
            return np.sum(diff)
        else:
            diff = diff + diff.transpose()
            diff[diff > 1] = 1  # Ignoring the double edges.
            return np.sum(diff) / 2
