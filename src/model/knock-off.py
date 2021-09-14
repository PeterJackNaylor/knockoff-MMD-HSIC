
import argparse
import numpy as np
from pandas import DataFrame

from knock_off import KnockOff

def load_npz(path):
    data = np.load(path)
    X = data['X']
    y = data['Y']
    return X, y

def false_discovery_rate(model, dataset="model_2a"):
    if dataset in ["model_0", "model_2a", "model_2b", "model_2c", "model_2d"]:
        correct_covariates = [0, 1, 2, 3]
    elif dataset in ["model_4a", "model_4b"]:
        correct_covariates = list(range(10))
    else:
        print("DATASET name not recognised")

    if model.n_features_out_ == 0:
        print("No feature selection process happened")
        return -1
    else:
        selected_features = model.alpha_indices_
        n_selected = len(selected_features)
        correct_covariates = [0, 1, 2, 3]
        intersection = list(set(selected_features) & set(correct_covariates))
        number_of_correct_positives = len(intersection)
        fdr = (n_selected - number_of_correct_positives) / n_selected
        return fdr

def f_fdp(t, w):
    num = (w <= -t).sum()
    den = max((w >= t).sum(), 1)
    return num / den 

def false_discovery_proportion(model):

    if model.n_features_out_ == 0:
        print("No feature selection process happened")
        return [None], [None]
    else:
        wjs = model.wjs_
        t_s = wjs.copy()
        t_s = [abs(w) for w in t_s]
        t_s.sort()
        fdp = [f_fdp(t, wjs) for t in t_s]
        return t_s, fdp

def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--t", type=str, default="PC")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--n_1", type=float, default=0.1)
    parser.add_argument("--d", type=int, default=10)
    parser.add_argument("--param", type=str, default=None)
    args = parser.parse_args()

    if args.param:
        d = dict(x.split("=") for x in args.param.split(";"))
        args.param_d = d
        args.param_d["AM"] = args.t
        args.param_d["alpha"] = args.alpha
        args.param_d["n_1"] = args.n_1
        args.param_d["d"] = args.d
        args.param += f";AM={args.t};alpha={args.alpha};n_1={args.n_1};d={args.d}"
    return args

def main():
    ## Load data
    opt = options()
    print("Loading data")
    X, y = load_npz("Xy.npz")
    print("Data loaded")

    ## Perform knock off procedure
    model = KnockOff(opt.alpha, measure_stat=opt.t)
    print("Starting fit process")
    model.fit(X, y, n1=opt.n_1, d=opt.d)
    print("Fit process finished")

    ## Record fdr and report parameters
    t_s, fdp = false_discovery_proportion(model)
    fdr = false_discovery_rate(model, dataset=opt.param_d["DATASET"])
    opt.param_d["fdr"] = fdr
    print(f"False discovery rate = {fdr}")
    DataFrame(opt.param_d, index=[0]).to_csv("fdr.csv", index=False)

    params = opt.param.replace(";", "--").replace(".", ",")
    DataFrame({"t": t_s, "fdp": fdp}).to_csv(f"fdp_{params}.csv", index=False)

if __name__ == "__main__":
    main()