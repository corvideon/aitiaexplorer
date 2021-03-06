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
import os

import pandas as pd
from pycausal.pycausal import pycausal
from tests.unit import TestAPI

from aitia_explorer.app import App
from aitia_explorer.feature_reduction.bayesian_gaussian_mixture_wrapper import BayesianGaussianMixtureWrapper
from aitia_explorer.feature_selection_runner import FeatureSelectionRunner
from aitia_explorer.target_data.loader import TargetData


class Test_App(TestAPI):
    """
    Tests for the aitia_explorer app.
    """
    bgmm = BayesianGaussianMixtureWrapper()

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'resources/data')

    def tearDown(self):
        pass

    def test_scm_load(self):
        aitia = App()
        scm1 = aitia.data.scm1()
        target_graph_str = str(scm1.cgm.draw())
        df = scm1.sample(1000)
        self.assertTrue(target_graph_str is not None)
        self.assertTrue(df is not None)

    def test_run_causal_analysis(self):
        pc = pycausal()
        pc.start_vm()
        aitia = App()
        data_dir = os.path.join(self.data_dir, "charity.txt")
        df = pd.read_table(data_dir, sep="\t")
        # just need a test graph
        dot_str = aitia.algo_runner.algo_pc(df, pc)
        # algo list
        algorithm_list = []
        algorithm_list.append(aitia.algo_runner.PC)
        algorithm_list.append(aitia.algo_runner.FCI)
        analysis_results = aitia._run_causal_algorithms(df,
                                                        algorithm_list=algorithm_list,
                                                        target_graph_str=dot_str,
                                                        pc=pc)
        self.assertTrue(analysis_results is not None)

    def test_run_full_analysis(self):
        # setup
        pc = pycausal()
        pc.start_vm()
        aitia = App()
        data_dir = os.path.join(self.data_dir, "charity.txt")
        df = pd.read_table(data_dir, sep="\t")

        # just need a test graph
        dot_str = aitia.algo_runner.algo_pc(df, pc)

        # feature selection algos
        feature_selection_list = []
        feature_selection_list.append(aitia.feature_selection.LINEAR_REGRESSION)
        feature_selection_list.append(aitia.feature_selection.PRINCIPAL_FEATURE_ANALYSIS)

        # causal algo list
        algorithm_list = []
        algorithm_list.append(aitia.algo_runner.PC)
        algorithm_list.append(aitia.algo_runner.FCI)
        analysis_results, summary_df, _ = aitia.run_analysis(df,
                                                          target_graph_str=dot_str,
                                                          n_features=4,
                                                          feature_selection_list=feature_selection_list,
                                                          algorithm_list=algorithm_list,
                                                          pc=pc)
        self.assertTrue(analysis_results is not None)
        self.assertTrue(summary_df is not None)

    def test_run_analysis_with_high_low(self):
        # setup
        pc = pycausal()
        pc.start_vm()
        aitia = App()
        data_dir = os.path.join(self.data_dir, "charity.txt")
        df = pd.read_table(data_dir, sep="\t")

        # just need a test graph
        dot_str = aitia.algo_runner.algo_pc(df, pc)

        # feature selection algos
        feature_selection_list = []
        feature_selection_list.append(aitia.feature_selection.LINEAR_REGRESSION)
        feature_selection_list.append(aitia.feature_selection.PRINCIPAL_FEATURE_ANALYSIS)

        # causal algo list
        algorithm_list = []
        algorithm_list.append(aitia.algo_runner.PC)
        algorithm_list.append(aitia.algo_runner.FCI)
        analysis_results, summary_df, _ = aitia.run_analysis_with_high_low(df,
                                                          target_graph_str=dot_str,
                                                          feature_high=5,
                                                          feature_low=3,
                                                          feature_selection_list=feature_selection_list,
                                                          algorithm_list=algorithm_list,
                                                          pc=pc)
        self.assertTrue(analysis_results is not None)
        self.assertTrue(summary_df is not None)

    def test_all_returned_features(self):
        feature_set = set()
        hepart_data = TargetData.hepar2_100_data()
        feature_set.update(FeatureSelectionRunner.random_forest_feature_reduction(hepart_data, 10))
        feature_set.update(FeatureSelectionRunner.pfa_feature_reduction(hepart_data, 10))
        feature_set.update(FeatureSelectionRunner.linear_regression_feature_reduction(hepart_data, 10))
        feature_set.update(FeatureSelectionRunner.xgboost_feature_reduction(hepart_data, 10))
        feature_set.update(FeatureSelectionRunner.rfe_feature_reduction(hepart_data, 10))
        df_reduced = self.bgmm.get_reduced_dataframe(hepart_data, list(feature_set))
        self.assertTrue(df_reduced is not None)
