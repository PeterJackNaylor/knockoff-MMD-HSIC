from .projection_correlation import projection_corr
from .tr import tr
from .hsic import HSIC, HSIC_norm
from .mmd import MMD, MMD_norm
from .pearson_correlation import pearson_correlation
from .distance_correlation import distance_corr


# https://github.com/vnmabus/dcor
__all__ = [
    "projection_corr", "tr", "distance_corr", "HSIC",
    "HSIC_norm", "MMD", "MMD_norm", "pearson_correlation"
]
