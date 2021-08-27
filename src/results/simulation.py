
import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
    args = parser.parse_args()

    return args

def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    # remove those which didn't select anything
    table = table.loc[table["fdr"] != -1]
    groups = table.groupby(["DATASET", "n", "p", "AM"])
    fig = go.Figure()
    for g_n, group in groups:
        alpha_group = group.groupby(['alpha'])
        mean = alpha_group.mean()
        sample_number = alpha_group.count()
        std = alpha_group.std()


        x = mean.index.sort_values()
        y = mean.loc[x, "fdr"]
        err = 1.96 * std.loc[x, "fdr"] / (sample_number.loc[x, "fdr"]) ** 0.5
        curve = go.Scatter(
            x=x,
            y=y,
            name=f"{g_n[0]}_n={g_n[1]}_p={int(g_n[2])}_am={g_n[3]}",
            error_y=dict(
                array=err)
            )
        fig.add_trace(curve)

    fig.write_html("simulation_plot.html")

if __name__ == "__main__":
    main()
