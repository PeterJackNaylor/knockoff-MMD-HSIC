from .projection_correlation import projection_corr
from .tr import tr
from .hsic import HSIC
from .mmd import MMD


from dcor import distance_correlation
# https://github.com/vnmabus/dcor
__all__ = ["projection_corr", "tr", "distance_correlation", "HSIC", "MMD"]
