"""
Implementation of algorithm 1 of paper Model-Free Feature
Screening and FDR Control with Knockoff Features with metrics
PC, HSIC and MMD.

"""

from copy import Error
import numpy as np

import numpy.typing as npt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from .utils import screen, build_knockoff, knock_off_check_parameters
from .association_measures import projection_corr, tr, distance_corr, MMD, HSIC

class KnockOff(BaseEstimator, TransformerMixin):
    """
    The KnockOff object is a transformer from the sklearn
    base object.
    :param alpha: float between 0 and 1. Sets the FDR rate.
    :param measure_stat: string, sets the association measure

    The model parameters once fitted will be alpha_indices.
    """

    def __init__(
        self, alpha: float = 1.0,
        measure_stat: str = "PC"
    ) -> None:
        super().__init__()
        self.alpha = alpha
        assert measure_stat in ["PC", "DC", "TR", "HSIC", "MMD"], "measure_stat incorrect"
        self.measure_stat = measure_stat

    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike, n1: float = 0.1, d: int = 1, seed: int = 42):
        """Fits model in a supervised manner following algorithm 1 in the paper
        *Model-free Feature Screening and FDR Control with Knockoff Features*
        by Liu et Al (2021).
        If d < n2 / 2 we do not perform the screening set to reduce the data.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        n1 : float between 0 and 1. Screening is applied on n1 percentage of 
        the initial dataset
        
        d : integer, sets the number of features to reduce the dataset in the 
        screening step
        """

        if seed:
            np.random.seed(seed)
            
        X, y = check_X_y(X, y)
        X = X.copy()
        y = np.expand_dims(y, axis=1)

        n, p = X.shape
        self.n_features_in_ = p
        stop, screening, set_one, set_two, msg = knock_off_check_parameters(n, p, n1, d)

        if stop:
            # raise ValueError(msg)
            print(msg)
            self.alpha_indices_ = []
            self.n_features_out_ = 0
            return self

        if screening:
            print("Starting screening")
            X1, y1 = X[set_one, :], y[set_one]
            X2, y2 = X[set_two, :], y[set_two]
            A_d_hat = screen(X1, y1, d, self.get_association_measure())

        else:
            print("No screening")
            X2 = X
            y2 = y
            A_d_hat = np.arange(p)

        # knock off step
        # construct knock off variables
        print("Starting knockoff step")
        wjs = build_knockoff(X2[:, A_d_hat], y2, self.get_association_measure())
        self.alpha_indices_, self.t_alpha_ = threshold_alpha(wjs, A_d_hat, self.alpha)
        self.wjs_ = wjs

        if len(self.alpha_indices_):
            print("selected features: ", self.alpha_indices_)
        else:
            print("No features were selected, returning empty set.")
        self.n_features_out_ = len(self.alpha_indices_)
        return self

    def transform(self, X, y=None):
        """Transforms an input dataset X into the reduce set of features
        given by the alpha_indices found by the fit method.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.
        """
        check_is_fitted(self, attributes=['alpha_indices_'])
        X = check_array(X)
        assert self.n_features_in_ == X.shape[1], "Same shape for fit and transform"
        return X[:, self.alpha_indices_]

    def fit_transform(self, X, y, **fit_params):
        """Fits and transforms an input dataset X and y.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.
        """

        return self.fit(X, y, **fit_params).transform(X, y)

    def get_association_measure(self):
        """Returns the correct association measure 
        given the attribute in __init__.
        """
        if self.measure_stat == "PC":
            f = projection_corr
        elif self.measure_stat == "TR":
            f = tr
        elif self.measure_stat == "HSIC":
            f = HSIC
        elif self.measure_stat == "MMD":
            f = MMD
        elif self.measure_stat == "DC":
            f = distance_corr
        else:
            raise ValueError(f"associative measure undefined {self.measure_stat}")
        return f

    def _more_tags(self):
        return {'stateless': True}


def threshold_alpha(Ws, w_indice, alpha):
    """
    Computes the set defined by equation 3.8
    TODO: better docstring

    Parameters
    ----------
    Ws : list like object corresponding to the estimator W_j
        for each feature.

    w_indice : numpy array like object corresponding to the indices
    of the W_j in the original dataset.

    alpha : float between 0 and 1. Sets the FDR rate.

    Returns
    -------
    indices : numpy array like corresponding to the selected features.

    t_alpha : float, which is the threshold used to select the set of active
    features.

    """
    t_max = max(Ws) + 1

    def fraction_3_6(t):
        num = (Ws <= -abs(t)).sum() + 1
        den = max((Ws >= abs(t)).sum(), 1)
        is_below_alpha = (num / den) <= alpha
        if is_below_alpha:
            return abs(t)
        else:
            return t_max

    t_alpha_list = list(map(fraction_3_6, Ws))
    t_alpha = min(t_alpha_list)
    indices = [w_indice[i] for i, el in enumerate(Ws) if el >= t_alpha]
    if t_max == t_alpha:
        t_alpha = np.inf
    return indices, t_alpha
