from .projection_correlation import projection_corr
from .tr import tr
from .hsic import (
    HSIC_linear, HSIC_linear_norm,
    HSIC_distance, HSIC_distance_norm,
    HSIC_rbf, HSIC_rbf_norm
)
from .mmd import (
    MMD_linear, MMD_linear_norm,
    MMD_distance, MMD_distance_norm,
    MMD_rbf, MMD_rbf_norm
)
from .pearson_correlation import pearson_correlation
from .distance_correlation import distance_corr


# https://github.com/vnmabus/dcor
__all__ = [
    "projection_corr", "tr", "distance_corr", 
    "HSIC_linear", "HSIC_linear_norm", "MMD_linear", "MMD_linear_norm", 
    "HSIC_distance", "HSIC_distance_norm", "MMD_distance", "MMD_distance_norm", 
    "HSIC_rbf", "HSIC_rbf_norm", "MMD_rbf", "MMD_rbf_norm",
    "pearson_correlation"
]
