import biom.table
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import os
from scipy.stats._stats_mstats_common import LinregressResult
from unittest import TestCase
from pysyndna import fit_linear_regression_models, \
    fit_linear_regression_models_for_qiita
from pysyndna.src.fit_syndna_models import SAMPLE_ID_KEY, SYNDNA_ID_KEY, \
    SYNDNA_POOL_MASS_NG_KEY, SYNDNA_INDIV_NG_UL_KEY, \
    SYNDNA_FRACTION_OF_POOL_KEY,  SYNDNA_INDIV_NG_KEY, \
    SYNDNA_TOTAL_READS_KEY, SYNDNA_POOL_NUM_KEY, \
    _validate_syndna_id_consistency, _validate_sample_id_consistency, \
    _calc_indiv_syndna_weights, _fit_linear_regression_models


class FitSyndnaModelsTest(TestCase):
    def assert_lingressresult_dict_almost_equal(self, d1, d2, places=7):
        """Assert that two dicts of LinregressResult are almost equal.

        Parameters
        ----------
        d1 : dict
            The first dict of LinregressResult to compare
        d2 : dict
            The second dict of LinregressResult to compare
        places : int, optional
            The number of decimal places to compare to

        Raises
        ------
        AssertionError
            If the dicts are not almost equal
        """
        self.assertIsInstance(d1, dict)
        self.assertIsInstance(d2, dict)
        self.assertEqual(d1.keys(), d2.keys())
        for k in d1.keys():
            self.assert_linregressresult_almost_equal(d1[k], d2[k], places)

    def assert_linregressresult_almost_equal(self, l1, l2, places=7):
        """Assert that two LinregressResult are almost equal.

        Parameters
        ----------
        l1 : dict
            The first LinregressResult to compare
        l2 : dict
            The second LinregressResult to compare
        places : int, optional
            The number of decimal places to compare to

        Raises
        ------
        AssertionError
            If the LinregressResults are not almost equal
        """
        self.assertIsInstance(l1, LinregressResult)
        self.assertIsInstance(l2, LinregressResult)
        self.assertEqual(len(l1), len(l2))
        for i in range(0, len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], places=places)

    def setUp(self):
        self.maxDiff = None
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_fit_linear_regression_models_for_qiita(self):
        prep_info_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            "sequencing_type": ["16S", "16S"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
            SYNDNA_POOL_NUM_KEY: [1, 1]
        }
        prep_info_df = pd.DataFrame(prep_info_dict)

        syndna_ids = ["p126", "p136", "p146", "p156", "p166", "p226",
                      "p236", "p246", "p256", "p266"]
        sample_ids = ["A", "B"]
        counts = np.array([[93135, 90897],
                           [15190, 15002],
                           [2447, 2421],
                           [308, 296],
                           [77, 77],
                           [149, 148],
                           [1075, 1059],
                           [3189, 3129],
                           [25347, 24856],
                           [237329, 230898]]
                          )
        input_biom = biom.table.Table(counts, syndna_ids, sample_ids)
        min_counts = 50

        expected_out = {
            'lin_regress_by_sample_id':
                'A:\n'
                '  intercept: -6.724238188489\n'
                '  intercept_stderr: 0.236197627825\n'
                '  pvalue: 1.42844e-07\n'
                '  rvalue: 0.986503097515\n'
                '  slope: 1.244876523791\n'
                '  stderr: 0.073054085503\n'
                'B:\n'
                '  intercept: -7.155318973708\n'
                '  intercept_stderr: 0.256395675584\n'
                '  pvalue: 1.50538e-07\n'
                '  rvalue: 0.986324179735\n'
                '  slope: 1.246759136044\n'
                '  stderr: 0.073657952553\n',
            'fit_syndna_models_log': ''
        }

        output_dict = fit_linear_regression_models_for_qiita(
            prep_info_df, input_biom, min_counts)

        self.assertDictEqual(expected_out, output_dict)

    def test_fit_linear_regression_models_for_qiita_w_alt_config(self):
        prep_info_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            "sequencing_type": ["16S", "16S"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
            SYNDNA_POOL_NUM_KEY: [1, 1]
        }
        prep_info_df = pd.DataFrame(prep_info_dict)

        syndna_ids = ["p126", "p136", "p146", "p156", "p166", "p226",
                      "p236", "p246", "p256", "p266"]
        sample_ids = ["A", "B"]
        counts = np.array([[93135, 90897],
                           [15190, 15002],
                           [2447, 2421],
                           [308, 296],
                           [77, 77],
                           [149, 148],
                           [1075, 1059],
                           [3189, 3129],
                           [25347, 24856],
                           [237329, 230898]]
                          )
        input_biom = biom.table.Table(counts, syndna_ids, sample_ids)
        min_counts = 50
        alt_config_fp = os.path.join(self.data_dir, 'alt_config.yml')

        expected_out = {
            'lin_regress_by_sample_id':
                'A:\n'
                '  intercept: -8.198448239722\n'
                '  intercept_stderr: 0.543935662662\n'
                '  pvalue: 1.287067e-05\n'
                '  rvalue: 0.958056670088\n'
                '  slope: 1.590774502959\n'
                '  stderr: 0.168235061352\n'
                'B:\n'
                '  intercept: -8.723558660515\n'
                '  intercept_stderr: 0.586319521146\n'
                '  pvalue: 1.2820953e-05\n'
                '  rvalue: 0.958097757898\n'
                '  slope: 1.593537551784\n'
                '  stderr: 0.168439250666\n',
            'fit_syndna_models_log': ''
        }

        output_dict = fit_linear_regression_models_for_qiita(
            prep_info_df, input_biom, min_counts, alt_config_fp)

        self.assertDictEqual(expected_out, output_dict)

    def test_fit_linear_regression_models_for_qiita_w_log_msgs(self):
        prep_info_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            "sequencing_type": ["16S", "16S"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
            SYNDNA_POOL_NUM_KEY: [1, 1]
        }
        prep_info_df = pd.DataFrame(prep_info_dict)

        syndna_ids = ["p126", "p136", "p146", "p156", "p166", "p226",
                      "p236", "p246", "p256", "p266"]
        sample_ids = ["A", "B"]
        counts = np.array([[93135, 90897],
                           [15190, 15002],
                           [2447, 2421],
                           [308, 296],
                           [77, 77],
                           [149, 148],
                           [1075, 1059],
                           [3189, 3129],
                           [25347, 24856],
                           [237329, 230898]]
                          )
        input_biom = biom.table.Table(counts, syndna_ids, sample_ids)
        min_counts = 200

        expected_out = {
            'lin_regress_by_sample_id':
                'A:\n'
                '  intercept: -6.767160120684\n'
                '  intercept_stderr: 0.301479875957\n'
                '  pvalue: 2.170514e-06\n'
                '  rvalue: 0.982777689569\n'
                '  slope: 1.256194910944\n'
                '  stderr: 0.089276147107\n'
                'B:\n'
                '  intercept: -7.196128673001\n'
                '  intercept_stderr: 0.326579863246\n'
                '  pvalue: 2.289073e-06\n'
                '  rvalue: 0.982512701026\n'
                '  slope: 1.25681918648\n'
                '  stderr: 0.090023307568\n',
            'fit_syndna_models_log':
                "The following syndnas were dropped because they had fewer "
                "than 200 total reads aligned:['p166']"
        }

        output_dict = fit_linear_regression_models_for_qiita(
            prep_info_df, input_biom, min_counts)

        self.assertDictEqual(expected_out, output_dict)

    def test_fit_linear_regression_models_for_qiita_w_pool_error(self):
        prep_info_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            "sequencing_type": ["16S", "16S"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
            SYNDNA_POOL_NUM_KEY: [1, 2]
        }
        prep_info_df = pd.DataFrame(prep_info_dict)

        syndna_ids = ["p126", "p136", "p146", "p156", "p166", "p226",
                      "p236", "p246", "p256", "p266"]
        sample_ids = ["A", "B"]
        counts = np.array([[93135, 90897],
                           [15190, 15002],
                           [2447, 2421],
                           [308, 296],
                           [77, 77],
                           [149, 148],
                           [1075, 1059],
                           [3189, 3129],
                           [25347, 24856],
                           [237329, 230898]]
                          )
        input_biom = biom.table.Table(counts, syndna_ids, sample_ids)
        min_counts = 50

        # NB: the error message is a regex, so we need to escape the brackets
        expected_err_msg = \
            r"Multiple syndna_pool_numbers found in prep info: \[1 2\]"

        with self.assertRaisesRegex(ValueError, expected_err_msg):
            fit_linear_regression_models_for_qiita(
                prep_info_df, input_biom, min_counts)

    def test_fit_linear_regression_models_for_qiita_w_col_error(self):
        prep_info_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            "sequencing_type": ["16S", "16S"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
            # missing the SYNDNA_POOL_NUM_KEY column
        }
        prep_info_df = pd.DataFrame(prep_info_dict)

        syndna_ids = ["p126", "p136", "p146", "p156", "p166", "p226",
                      "p236", "p246", "p256", "p266"]
        sample_ids = ["A", "B"]
        counts = np.array([[93135, 90897],
                           [15190, 15002],
                           [2447, 2421],
                           [308, 296],
                           [77, 77],
                           [149, 148],
                           [1075, 1059],
                           [3189, 3129],
                           [25347, 24856],
                           [237329, 230898]]
                          )
        input_biom = biom.table.Table(counts, syndna_ids, sample_ids)
        min_counts = 50

        # NB: the error message is a regex, so we need to escape the brackets
        expected_err_msg = \
            r"prep info is missing required column\(s\): " \
            r"\{'syndna_pool_number'\}"

        with self.assertRaisesRegex(ValueError, expected_err_msg):
            fit_linear_regression_models_for_qiita(
                prep_info_df, input_biom, min_counts)

    def test_fit_linear_regression_models(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }
        min_count = 50

        expected_out = {
            'A': LinregressResult(
                slope=1.244876523791319, intercept=-6.7242381884894655,
                rvalue=0.9865030975156575, pvalue=1.428443560659758e-07,
                stderr=0.07305408550335003,
                intercept_stderr=0.2361976278251443),
            'B': LinregressResult(
                slope=1.24675913604407, intercept=-7.155318973708384,
                rvalue=0.9863241797356326, pvalue=1.505381146809759e-07,
                stderr=0.07365795255302438,
                intercept_stderr=0.2563956755844754)
        }

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        out_linregress_dict, out_msgs = fit_linear_regression_models(
            syndna_concs_df,
            sample_syndna_weights_and_total_reads_df,
            reads_per_syndna_per_sample_df, min_count)

        self.assert_lingressresult_dict_almost_equal(
            expected_out, out_linregress_dict)
        self.assertEqual([], out_msgs)

    def test_fit_linear_regression_models_w_log_msgs(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B", "C"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417, 2606004],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2, 0.3],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }
        min_count = 200

        expected_out_dict = {
            'A': LinregressResult(
                slope=1.2561949109446753, intercept=-6.7671601206840855,
                rvalue=0.982777689569875, pvalue=2.1705143708536327e-06,
                stderr=0.08927614710714807,
                intercept_stderr=0.30147987595768355),
            'B': LinregressResult(
                slope=1.2568191864801976, intercept=-7.196128673001381,
                rvalue=0.9825127010266727, pvalue=2.2890733334160456e-06,
                stderr=0.09002330756867402,
                intercept_stderr=0.32657986324660143)
        }
        expected_out_msgs = [
            "The following sample ids were in the experiment info but not in "
            "the data: ['C']",
            "The following syndnas were dropped because they had fewer than "
            "200 total reads aligned:['p166']"
        ]

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        out_linregress_dict, out_msgs = fit_linear_regression_models(
            syndna_concs_df,
            sample_syndna_weights_and_total_reads_df,
            reads_per_syndna_per_sample_df, min_count)

        self.assert_lingressresult_dict_almost_equal(
            expected_out_dict, out_linregress_dict)
        self.assertEqual(expected_out_msgs, out_msgs)

    def test_fit_linear_regression_models_w_sample_error(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A"],
            SYNDNA_TOTAL_READS_KEY: [3216923],
            SYNDNA_POOL_MASS_NG_KEY: [0.25],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }
        min_count = 200

        expected_err_msg = \
            r"Found sample ids in reads_per_syndna_per_sample_df that were " \
            r"not in sample_syndna_weights_and_total_reads_df: \{'B'\}"

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        with self.assertRaisesRegex(ValueError, expected_err_msg):
            fit_linear_regression_models(
                syndna_concs_df,
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df, min_count)

    def test_fit_linear_regression_models_w_syndna_config_error(self):
        # syndnas in the data that aren't in the config

        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256",],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1],
        }

        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B", "C"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417, 2606004],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2, 0.3],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        min_count = 200

        expected_err_msg = \
            r"Detected 1 syndna feature\(s\) in the read data that " \
            r"were not in the config: {'p266'}"

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        with self.assertRaisesRegex(ValueError, expected_err_msg):
            fit_linear_regression_models(
                syndna_concs_df,
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df, min_count)

    def test_fit_linear_regression_models_w_syndna_data_error(self):
        # syndnas in the config that aren't in the data

        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856],
        }

        min_count = 200

        expected_err_msg = \
            r"Missing the following 1 required syndna feature\(s\) in the " \
            r"read data: \{'p266'\}"

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        with self.assertRaisesRegex(ValueError, expected_err_msg):
            fit_linear_regression_models(
                syndna_concs_df,
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df, min_count)

    def test__validate_syndna_id_consistency(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        try:
            _validate_syndna_id_consistency(
                syndna_concs_df, reads_per_syndna_per_sample_df)
        except ValueError:
            self.fail("Raised ValueError incorrectly")

    def test__validate_syndna_id_consistency_w_error_missing_data(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856],
        }

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        # NB: the error message is a regex, so we need to escape the brackets
        err_msg = \
            r"Missing the following 1 required syndna feature\(s\) " \
            r"in the read data: \{'p266'\}"
        with self.assertRaisesRegex(ValueError, err_msg):
            _validate_syndna_id_consistency(
                syndna_concs_df,
                reads_per_syndna_per_sample_df)

    def test__validate_syndna_id_consistency_w_error_missing_info(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        # NB: the error message is a regex, so we need to escape the brackets
        err_msg = r"Detected 1 syndna feature\(s\) in the read data " \
                  r"that were not in the config: \{'p266'\}"
        with self.assertRaisesRegex(ValueError, err_msg):
            _validate_syndna_id_consistency(
                syndna_concs_df,
                reads_per_syndna_per_sample_df)

    def test__validate_sample_id_consistency(self):
        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        try:
            output = _validate_sample_id_consistency(
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df)
        except ValueError:
            self.fail("Raised ValueError incorrectly")

        # all samples are in both, so no extras reported
        self.assertIsNone(output)

    def test__validate_sample_id_consistency_w_output(self):
        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A", "B", "C"],
            SYNDNA_TOTAL_READS_KEY: [3216923, 1723417, 2606004],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2, 0.3],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        try:
            output = _validate_sample_id_consistency(
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df)
        except ValueError:
            self.fail("Raised ValueError incorrectly")

        # sample C is in sample info but not in sequencing results;
        # for example, maybe it failed to sequence
        self.assertEqual(["C"], output)

    def test__validate_sample_id_consistency_w_error(self):
        sample_syndna_weights_and_total_reads_dict = {
            SAMPLE_ID_KEY: ["A"],
            SYNDNA_TOTAL_READS_KEY: [3216923],
            SYNDNA_POOL_MASS_NG_KEY: [0.25],
        }

        reads_per_syndna_per_sample_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            "A": [93135, 15190, 2447, 308, 77, 149, 1075, 3189, 25347, 237329],
            "B": [90897, 15002, 2421, 296, 77, 148, 1059, 3129, 24856, 230898],
        }

        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            sample_syndna_weights_and_total_reads_dict)
        reads_per_syndna_per_sample_df = pd.DataFrame(
            reads_per_syndna_per_sample_dict)

        err_msg = "Found sample ids in reads_per_syndna_per_sample_df " \
                  "that were not in sample_syndna_weights_and_total_reads_df"
        with self.assertRaisesRegex(ValueError, err_msg):
            _validate_sample_id_consistency(
                sample_syndna_weights_and_total_reads_df,
                reads_per_syndna_per_sample_df)

    def test__calc_indiv_syndna_weights(self):
        syndna_concs_dict = {
            SYNDNA_ID_KEY: ["p126", "p136", "p146", "p156", "p166", "p226",
                            "p236", "p246", "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [1, 0.1, 0.01, 0.001, 0.0001, 0.0001,
                                     0.001, 0.01, 0.1, 1],
        }

        working_dict = {
            SAMPLE_ID_KEY: ["A1_pool1_Fwd", "A1_pool1_Rev", "A1_pool1_Fwd",
                            "A1_pool1_Rev", "A1_pool1_Fwd", "A1_pool1_Rev",
                            "A1_pool1_Fwd", "A1_pool1_Rev", "A1_pool1_Fwd",
                            "A1_pool1_Rev", "A1_pool1_Fwd", "A1_pool1_Rev",
                            "A1_pool1_Fwd", "A1_pool1_Rev", "A1_pool1_Fwd",
                            "A1_pool1_Rev", "A1_pool1_Fwd", "A1_pool1_Rev",
                            "A1_pool1_Fwd", "A1_pool1_Rev"],
            SYNDNA_ID_KEY: ["p126", "p126", "p136", "p136", "p146", "p146",
                            "p156", "p156", "p166", "p166", "p226", "p226",
                            "p236", "p236", "p246", "p246", "p256", "p256",
                            "p266", "p266"],
            SYNDNA_POOL_MASS_NG_KEY: [0.25, 0.2, 0.25, 0.2, 0.25, 0.2, 0.25,
                                      0.2, 0.25, 0.2, 0.25, 0.2, 0.25, 0.2,
                                      0.25, 0.2, 0.25, 0.2, 0.25, 0.2]
        }

        expected_addl_dict = {
            SYNDNA_INDIV_NG_UL_KEY: [1, 1, 0.1, 0.1, 0.01, 0.01, 0.001, 0.001,
                                     0.0001, 0.0001, 0.0001, 0.0001, 0.001,
                                     0.001, 0.01, 0.01, 0.1, 0.1, 1, 1],
            SYNDNA_FRACTION_OF_POOL_KEY: [0.4500045, 0.4500045, 0.04500045,
                                          0.04500045, 0.004500045, 0.004500045,
                                          0.000450005, 0.000450005,
                                          4.50005E-05, 4.50005E-05,
                                          4.50005E-05, 4.50005E-05,
                                          0.000450005, 0.000450005,
                                          0.004500045, 0.004500045,
                                          0.04500045, 0.04500045, 0.4500045,
                                          0.4500045],
            SYNDNA_INDIV_NG_KEY: [0.112501125, 0.0900009, 0.011250113,
                                  0.00900009, 0.001125011, 0.000900009,
                                  0.000112501, 9.00009E-05, 1.12501E-05,
                                  9.00009E-06, 1.12501E-05, 9.00009E-06,
                                  0.000112501, 9.00009E-05, 0.001125011,
                                  0.000900009, 0.011250113, 0.00900009,
                                  0.112501125, 0.0900009]
        }

        syndna_concs_df = pd.DataFrame(syndna_concs_dict)
        working_df = pd.DataFrame(working_dict)

        output_df = _calc_indiv_syndna_weights(syndna_concs_df, working_df)

        expected_dict = working_dict | expected_addl_dict
        expected_df = pd.DataFrame(expected_dict)
        assert_frame_equal(expected_df, output_df)

    def test__fit_linear_regression_models(self):
        input_fp = os.path.join(self.data_dir, 'modelling_input.tsv')
        working_df = pd.read_csv(input_fp, sep="\t", comment="#")

        output = _fit_linear_regression_models(working_df)

        expected_fp = os.path.join(self.data_dir, 'modelling_output.tsv')
        expected_df = pd.read_csv(expected_fp, sep="\t", comment="#")

        for k, v in output.items():
            self.assertIsInstance(v, LinregressResult)

            item_mask = expected_df["ID"] == k
            expected_slope = expected_df.loc[item_mask, "b_slope"].iloc[0]
            expected_intercept = expected_df.loc[
                item_mask, "a_intercept"].iloc[0]
            self.assertAlmostEqual(expected_slope, v.slope)
            self.assertAlmostEqual(expected_intercept, v.intercept)
        # next model
