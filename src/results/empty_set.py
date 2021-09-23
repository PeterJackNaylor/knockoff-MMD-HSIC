
import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
    args = parser.parse_args()

    return args

row_dic = {100: 1, 500: 2, 5000: 3}
col_dic = {100: 1, 500: 2, 1000: 3}
colors = {"MMD": "rgb(0, 186, 56)",
        "TR": "rgb(245, 100, 227)",
        "HSIC": "rgb(183, 159, 0)",
        "pearson_correlation": "rgb(97, 156, 255)",
        "PC": "rgb(0, 191, 196)",
        "DC": "rgb(248, 118, 109)"}

def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    groups = table.groupby(['AM', 'alpha'])
    for am_alpha, df_group in groups:
        n = df_group.shape[0]
        no_selected_features = (df_group['fdr'] == -1).sum()
    # remove those which didn't select anything