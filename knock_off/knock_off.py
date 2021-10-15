"""
Implementation of algorithm 1 of paper Model-Free Feature
Screening and FDR Control with Knockoff Features with metrics
PC, HSIC and MMD.

"""


import numpy as np

import numpy.typing as npt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from .utils import build_knockoff, knock_off_check_parameters, screen
from . import association_measures as am


available_am = ["PC", "DC", "TR", "HSIC", "MMD", "pearson_correlation"]
kernel_am = ["HSIC", "MMD"]
available_kernels = ["distance", "gaussian", "linear"]


class KnockOff(BaseEstimator, TransformerMixin):
    """
    The KnockOff object is a transformer from the sklearn
    base object.
    :param alpha: float between 0 and 1. Sets the FDR rate.
    :param measure_stat: string, sets the association measure

    The model parameters once fitted will be alpha_indices.
    """

    def __init__(
        self,
        alpha: float = 1.0,
        measure_stat: str = "PC",
        kernel: str = "linear",
        normalised: bool = False,
        normalise_input: bool = True,
    ) -> None:
        super().__init__()
        self.alpha = alpha
        assert measure_stat in available_am, "measure_stat incorrect"
        assert kernel in available_kernels, "kernel incorrect"
        self.measure_stat = measure_stat
        self.kernel = kernel
        self.normalised = normalised
        self.normalise_input = normalise_input

    def get_assoc(self, x, y):

        args = {}
        if self.measure_stat in kernel_am:
            args["kernel"] = self.kernel
            args["normalised"] = self.normalised

        if self.normalise_input:
            x = x / np.linalg.norm(x, ord=2, axis=0)

        assoc_func = self.get_association_measure()

        return assoc_func(x, y, **args)

    def fit(
        self,
        X: npt.ArrayLike,
        y: npt.ArrayLike,
        n1: float = 0.1,
        d: int = 1,
        seed: int = 42,
    ):
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

        Returns
        -------
        Itself, to comply with sklearn rules.
        """

        if seed:
            np.random.seed(seed)

        X, y = check_X_y(X, y)
        X = X.copy()
        y = np.expand_dims(y, axis=1)

        n, p = X.shape
        self.n_features_in_ = p
        stop, screening, s1, s2, msg = knock_off_check_parameters(n, p, n1, d)

        if stop:
            # raise ValueError(msg)
            print(msg)
            self.alpha_indices_ = []
            self.n_features_out_ = 0
            return self

        if screening:
            print("Starting screening")
            X1, y1 = X[s1, :], y[s1]
            X2, y2 = X[s2, :], y[s2]

            self.A_d_hat_, self.screen_scores_ = screen(
                X1, y1, d, self.get_assoc
            )
            screen_scores = None

        else:
            print("No screening")
            X2, y2 = X, y

            if self.normalise_input:
                X2 = X2 / np.linalg.norm(X2, ord=2, axis=0)

            self.A_d_hat_, self.screen_scores_ = screen(
                X2, y2, d, self.get_assoc
            )
            screen_scores = self.screen_scores_[self.A_d_hat_]

        # knock off step
        # construct knock off variables
        print("Starting knockoff step")
        self.wjs_ = build_knockoff(
            X2[:, self.A_d_hat_],
            y2,
            self.get_assoc, prescreened=screen_scores
        )

        alpha_thres = self.alpha_threshold(self.alpha)
        self.alpha_indices_ = alpha_thres
        self.t_alpha_ = alpha_thres
        self.n_features_out_ = alpha_thres
        return self

    def alpha_threshold(self, alpha):
        """
        Computes the selected features with respect to alpha.

        Parameters
        ----------
        alpha : threshold value to use for post inference selection.

        Returns
        -------
        A 3 element tuple where:
            1 - indices corresponding to indexes of the chosen features in
            the original array.
            2 - the threshold value.
            3 - the number of selected features.

        """
        alpha_indices_, t_alpha_ = threshold_alpha(
            self.wjs_, self.A_d_hat_, alpha
        )
        if len(alpha_indices_):
            print("selected features: ", alpha_indices_)
        else:
            print("No features were selected, returning empty set.")
        n_features_out_ = len(alpha_indices_)
        return alpha_indices_, t_alpha_, n_features_out_

    def transform(self, X, y=None):
        """Transforms an input dataset X into the reduce set of features
        given by the alpha_indices found by the fit method.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        Returns
        -------
        A sliced X where we only retain the selected features.
        """
        check_is_fitted(self, attributes=["alpha_indices_"])
        X = check_array(X)
        msg = "Same shape for fit and transform"
        assert self.n_features_in_ == X.shape[1], msg
        return X[:, self.alpha_indices_]

    def fit_transform(self, X, y, **fit_params):
        """Fits and transforms an input dataset X and y.

        Parameters
        ----------
        X : numpy array like object where the rows correspond to the samples
            and the columns to features.

        y : numpy array like, which can be multi-dimensional.

        Returns
        -------
        The new version of X corresponding to the selected features.
        """

        return self.fit(X, y, **fit_params).transform(X, y)

    def get_association_measure(self):
        """Returns the correct association measure
        given the attribute in __init__.
        """
        if self.measure_stat == "PC":
            f = am.projection_corr
        elif self.measure_stat == "TR":
            f = am.tr
        elif self.measure_stat == "HSIC":
            f = am.HSIC
        elif self.measure_stat == "MMD":
            f = am.MMD
        elif self.measure_stat == "DC":
            f = am.distance_corr
        elif self.measure_stat == "pearson_correlation":
            f = am.pearson_correlation
        else:
            error_msg = f"associative measure undefined {self.measure_stat}"
            raise ValueError(error_msg)
        return f

    def _more_tags(self):
        return {"stateless": True}


def threshold_alpha(Ws, w_indice, alpha):
    """
    Computes the set defined by equation 3.8
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

    ts = np.sort(abs(Ws))

    def fraction_3_6(t):
        num = (Ws <= -abs(t)).sum() + 1
        den = max((Ws >= abs(t)).sum(), 1)
        return num / den

    fraction_3_6_v = np.vectorize(fraction_3_6)
    fdp = fraction_3_6_v(ts)

    t_alpha = np.where(fdp <= alpha)
    if t_alpha[0].size == 0:
        # no one selected..
        t_alpha_min = np.inf
    else:
        t_alpha_min = min(ts[t_alpha])
    indices = w_indice[np.where(Ws >= t_alpha_min)[0]]
    return indices, t_alpha
