#
# This file is part of AitiaExplorer and is released under the FreeBSD License.
#
# Copyright (c) 2020, Seamus Brady <seamus@corvideon.ie>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.#

import logging
import pyAgrum as gum
import tempfile

from aitia_explorer.causal_algorithms.algorithm_constants import AlgorithmConstants
from aitia_explorer.util.graph_util import GraphUtil

_logger = logging.getLogger(__name__)


class MIICAlgorithm():
    """
    Returns a list of unobserved latent edges from a dataframe.
    MIIC (Multivariate Information based Inductive Causation) combines constraint-based
    and information-theoretic approaches to disentangle direct from indirect effects
    amongst correlated variables, including cause-effect relationships and the effect of unobserved latent causes..

    See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5685645/
    """

    def __init__(self):
        pass

    @staticmethod
    def run(df, pc=None):
        """
        Run the algorithm against the dataframe and gets a list of unobserved latent edges.
        """
        try:
            fp = tempfile.NamedTemporaryFile(suffix='.csv')
            df.to_csv(fp.name, encoding='utf-8', index=False)
            learner = gum.BNLearner(fp.name)
            learner.useMIIC()
            bn = learner.learnBN()
            latent_edges = []
            latent_edges.extend([(bn.variable(i).name(),
                                  bn.variable(j).name()) for (i,j) in learner.latentVariables()])
            return latent_edges
        except Exception as e:
            _logger.error(str(e))
            print(str(e))
        return None
