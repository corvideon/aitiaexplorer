"""
TBD Header
"""
import logging

from aitia_explorer.algorithms.bayes_est_algorithm import BayesEstAlgorithm
from aitia_explorer.algorithms.fci_algorithm import FCIAlgorithm
from aitia_explorer.algorithms.fges_algorithm import FGESAlgorithm
from aitia_explorer.algorithms.gfci_algorithm import GFCIAlgorithm
from aitia_explorer.algorithms.pc_algorithm import PCAlgorithm
from aitia_explorer.algorithms.rfci_algorithm import RFCIAlgorithm

_logger = logging.getLogger(__name__)


class PyCausalWrapper():
    """
    Class that wraps py-causal.
    """

    def __init__(self):
        pass

    def get_all_algorithms(self):
        return [self.algo_bayes_est,
                self.algo_fci,
                self.algo_pc,
                self.algo_fges_continuous,
                self.algo_fges_discrete,
                self.algo_fges_mixed,
                self.algo_gfci_continuous,
                self.algo_gfci_discrete,
                self.algo_gfci_mixed,
                self.algo_rfci_continuous,
                self.algo_rfci_discrete,
                self.algo_rfci_mixed
                ]

    # -------------------------------------------------------------------------------------------------
    #                   The methods below run the causal discovery algorithms
    # -------------------------------------------------------------------------------------------------

    ############### BayesEst ##################
    def algo_bayes_est(self, df, pc=None):
        return BayesEstAlgorithm.run(df, pc)

    ############### FCI ##################
    def algo_fci(self, df, pc=None):
        return FCIAlgorithm.run(df, pc)

    ############### PC ##################
    def algo_pc(self, df, pc=None):
        return PCAlgorithm.run(df, pc)

    ############### FGES ##################
    def algo_fges_continuous(self, df, pc=None):
        return FGESAlgorithm.run_continuous(df, pc)

    def algo_fges_discrete(self, df, pc=None):
        return FGESAlgorithm.run_discrete(df, pc)

    def algo_fges_mixed(self, df, pc=None):
        return FGESAlgorithm.run_mixed(df, pc)

    ############### GFCI ##################
    def algo_gfci_continuous(self, df, pc=None):
        return GFCIAlgorithm.run_continuous(df, pc)

    def algo_gfci_discrete(self, df, pc=None):
        return GFCIAlgorithm.run_discrete(df, pc)

    def algo_gfci_mixed(self, df, pc=None):
        return GFCIAlgorithm.run_mixed(df, pc)

    ############### RFCI ##################
    def algo_rfci_continuous(self, df, pc=None):
        return RFCIAlgorithm.run_continuous(df, pc)

    def algo_rfci_discrete(self, df, pc=None):
        return RFCIAlgorithm.run_discrete(df, pc)

    def algo_rfci_mixed(self, df, pc=None):
        return RFCIAlgorithm.run_mixed(df, pc)