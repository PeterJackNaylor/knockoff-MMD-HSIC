from .projection_correlation import projection_corr
from .tr import tr
from .hsic import HSIC
from .mmd import MMD
from .distance_correlation import distance_corr


# https://github.com/vnmabus/dcor
__all__ = ["projection_corr", "tr", "distance_corr", "HSIC", "MMD"]
