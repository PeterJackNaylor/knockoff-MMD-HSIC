
import argparse
import numpy as np
from pandas import DataFrame, Series

from knock_off import KnockOff, association_measures

def load_npz(path):
    data = np.load(path)
    X = data['X']
    y = data['Y']
    return X, y

def top_k(wjs, S):
    S = set(S)
    n = len(wjs)
    sorted_features = wjs.argsort()[-n:][::-1]

    for i in range(len(S), n, 1):
        if set(S).issubset(sorted_features[:i]):
            break
    return i + 1

def minimum_model_size_including_active(model, dataset="model_2a"):
    if dataset in ["model_0", "model_2a", "model_2b", "model_2c", "model_2d"]:
        correct_covariates = [0, 1, 2, 3]
    elif dataset in ["model_4a", "model_4b"]:
        correct_covariates = list(range(10))
    else:
        print("DATASET name not recognised")
    
    screening_score = model.screen_features_

    k0 = top_k(screening_score, correct_covariates)
    return k0


def false_discovery_rate(selected_features, dataset="model_2a"):
    if dataset in ["model_0", "model_2a", "model_2b", "model_2c", "model_2d"]:
        correct_covariates = [0, 1, 2, 3]
    elif dataset in ["model_4a", "model_4b"]:
        correct_covariates = list(range(10))
    else:
        print("DATASET name not recognised")

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

# def false_discovery_proportion(n_features_out, wjs):

#     if n_features_out == 0:
#         print("No feature selection process happened")
#         return [None], [None]
#     else:
#         t_s = wjs.copy()
#         t_s = [abs(w) for w in t_s]
#         t_s.sort()
#         fdp = [f_fdp(t, wjs) for t in t_s]
#         return t_s, fdp

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
        args.param += f";AM={args.t};n_1={args.n_1};d={args.d}"
    return args

def main():
    ## Load data
    opt = options()
    print("Loading data")
    X, y = load_npz("Xy.npz")
    print("Data loaded")

    ## Perform knock off procedure
    model = KnockOff(0.1, measure_stat=opt.t)
    print("Starting fit process")
    model.fit(X, y, n1=opt.n_1, d=opt.d)
    print("Fit process finished")

    # Get minimum model size containing true features
    k0 = minimum_model_size_including_active(model, dataset=opt.param_d["DATASET"])
    opt.param_d["k0"] = k0
        
    opt.param_d["fdr"] = 0

    pd_fdr = DataFrame(columns=opt.param_d.keys(), index=list(range(10, 95, 5)))

    for alpha in range(10, 95, 5):
        alpha_ind, _, _ = model.alpha_threshold(alpha / 100)
        # t_s, fdp = false_discovery_proportion(n_feat, model.wjs_)
        fdr = false_discovery_rate(alpha_ind, dataset=opt.param_d["DATASET"])
        print(f"False discovery rate = {fdr} for alpha = {alpha}")
        opt.param_d["fdr"] = fdr
        opt.param_d["alpha"] = alpha / 100
        pd_fdr.loc[alpha] = Series(opt.param_d)
    
    # Record fdr and report parameters    
    pd_fdr.to_csv("fdr.csv", index=False)

if __name__ == "__main__":
    main()