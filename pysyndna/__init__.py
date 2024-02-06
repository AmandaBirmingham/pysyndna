from pysyndna.src.fit_syndna_models import fit_linear_regression_models, \
    fit_linear_regression_models_for_qiita
from pysyndna.src.calc_cell_counts import calc_ogu_cell_counts_biom, \
    calc_ogu_cell_counts_per_g_of_sample_for_qiita
from pysyndna.src.quant_orfs import \
    calc_copies_of_ogu_orf_ssrna_per_g_sample, \
    calc_copies_of_ogu_orf_ssrna_per_g_sample_for_qiita

__all__ = ['fit_linear_regression_models',
           'fit_linear_regression_models_for_qiita',
           'calc_ogu_cell_counts_biom',
           'calc_ogu_cell_counts_per_g_of_sample_for_qiita',
           'calc_copies_of_ogu_orf_ssrna_per_g_sample',
           'calc_copies_of_ogu_orf_ssrna_per_g_sample_for_qiita']

from . import _version
__version__ = _version.get_versions()['version']
