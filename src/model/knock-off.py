import argparse
import numpy as np
from pandas import DataFrame, Series

from knock_off import KnockOff


def load_npz(path):
    data = np.load(path)
    X = data["X"]
    y = data["Y"]
    return X, y


def top_k(wjs, S):
    S = set(S)
    n = len(wjs)
    sorted_features = wjs.argsort()[-n:][::-1]

    for i in range(len(S), n, 1):
        if set(S).issubset(sorted_features[:i]):
            break
    return i + 1


def determine_covariate(dataset):
    if dataset in ["model_1a", "model_2a", "model_2b", "model_2d", "model_2e"]:
        correct_covariates = [0, 1, 2, 3]
    elif dataset in [
        "model_1b",
        "model_1c",
        "model_2c",
        "model_3a",
        "model_3b",
        "model_3c",
    ]:
        correct_covariates = list(range(10))
    else:
        correct_covariates = []
        print("DATASET name not recognised")
    return correct_covariates


def minimum_model_size_including_active(model, dataset="model_1a"):

    correct_covariates = determine_covariate(dataset)
    screening_score = model.screen_scores_

    k0 = top_k(screening_score, correct_covariates)
    return k0


def false_discovery_rate(selected_features, dataset="model_1a"):

    correct_covariates = determine_covariate(dataset)

    if len(selected_features) == 0:
        print("No feature selection process happened")
        return -1
    else:
        n_selected = len(selected_features)
        intersection = list(set(selected_features) & set(correct_covariates))
        number_of_correct_positives = len(intersection)
        fdr = (n_selected - number_of_correct_positives) / n_selected
        return fdr


def f_fdp(t, w):
    num = (w <= -t).sum()
    den = max((w >= t).sum(), 1)
    return num / den


def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--t", type=str, default="PC")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--n_1", type=float, default=0.1)
    parser.add_argument("--d", type=int, default=10)
    parser.add_argument("--xy", type=str, default="Xy.npz")
    parser.add_argument("--param", type=str, default=None)
    parser.add_argument("--kernel", type=str, default="linear")
    parser.add_argument("--normalise", type=int, default=0)
    args = parser.parse_args()

    if args.param:
        d = dict(x.split("=") for x in args.param.split(";"))
        args.param_d = d
        args.param_d["AM"] = args.t
        args.param_d["alpha"] = args.alpha
        args.param_d["n_1"] = args.n_1
        args.param_d["d"] = args.d
        args.param_d["normalise"] = args.normalise
        args.param_d["kernel"] = args.kernel
        args.param += f";AM={args.t};n_1={args.n_1};d={args.d}"
    args.normalise = args.normalise == 1
    return args


def main():
    # Load data
    opt = options()
    print("Loading data")
    X, y = load_npz(opt.xy)
    dataset = opt.param_d["DATASET"]
    print("Data loaded")

    # Perform knock off procedure
    model = KnockOff(
        0.1,  # not really important as we loop over alpha afterwards
        measure_stat=opt.t,
        kernel=opt.kernel,
        normalised=opt.normalise,
    )
    print("Starting fit process")
    model.fit(X, y, n1=opt.n_1, d=opt.d)
    print("Fit process finished")

    print("Saving files..")
    # Record Wjs.
    wjs = {"AM": opt.t, "feature": model.A_d_hat_, "wj": model.wjs_}
    pd_features = DataFrame(wjs)
    pd_features.to_csv("wjs.csv", index=False)

    # Get minimum model size containing true features
    k0 = minimum_model_size_including_active(model, dataset=dataset)
    opt.param_d["k0"] = k0

    opt.param_d["fdr"] = 0
    opt.param_d["features"] = ""

    pd_fdr = DataFrame(columns=opt.param_d.keys())

    for alpha in range(10, 95, 5):
        alpha = alpha / 100
        alpha_ind, _, _ = model.alpha_threshold(alpha)
        fdr = false_discovery_rate(alpha_ind, dataset=dataset)
        print(f"False discovery rate = {fdr} for alpha = {alpha}")
        opt.param_d["fdr"] = fdr
        opt.param_d["alpha"] = alpha
        opt.param_d["features"] = ",".join([str(x) for x in alpha_ind])
        pd_fdr.loc[alpha] = Series(opt.param_d)

    # Record fdr and report parameters
    pd_fdr.to_csv("fdr.csv", index=False)


if __name__ == "__main__":
    main()
