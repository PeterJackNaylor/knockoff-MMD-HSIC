
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


def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    groups = table.groupby(['AM'])
    bars = []
    alphas = table['alpha'].unique()


    for am, df_group in groups:
        n = df_group.shape[0]
        missing = (df_group.loc[df_group['fdr'] == -1]).groupby('alpha').count()[['n']]

        for alp in alphas:
            if alp not in missing.index:
                missing.loc[alp, "n"] = 0


        bars.append(go.Bar(x=alphas, y=missing['n']))
    fig = go.Figure(bars)
    fig.write_html("empty_set.html")
    
    # remove those which didn't select anything
if __name__ == "__main__":
    main()
