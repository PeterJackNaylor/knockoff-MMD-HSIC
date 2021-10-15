import os
import argparse
import pandas as pd
import plotly.graph_objects as go

from colors import color_dictionnary, kernel_colours


def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
    parser.add_argument("--kernels", type=int, default=0)
    parser.add_argument("--name", type=str, default="")

    args = parser.parse_args()

    return args


row_dic = {100: 1, 500: 2, 5000: 3}
col_dic = {100: 1, 500: 2, 1000: 3}


def main():
    # Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    groups = table.groupby(["AM", "normalise", "kernel"])
    bars = []
    alphas = table["alpha"].unique()
    only_kernel = opt.kernels == 1

    if not os.path.exists("images"):
        os.mkdir("images")

    for am_k_n, df_group in groups:
        name = am_k_n[0]
        kernel = am_k_n[2]
        normalised = am_k_n[1] == 1
        if only_kernel:
            if name not in ["HSIC", "MMD"]:
                continue
        else:
            if name in ["HSIC", "MMD"] and kernel != "gaussian":
                continue

        n = df_group.shape[0] / len(alphas)
        empty_df = df_group.loc[df_group["fdr"] == -1]
        missing = (empty_df).groupby("alpha").count()[["n"]] / n

        for alp in alphas:
            if alp not in missing.index:
                missing.loc[alp, "n"] = 0
        name_color = name
        s2 = ""
        s3 = ""
        if name in ["HSIC", "MMD"]:
            s1 = "" if int(normalised) == 0 else "_norm"
            s3 = "" if int(normalised) == 0 else "n"
            s2 = f" ({kernel})"
            name_color += s1

        if only_kernel:
            marker_color = kernel_colours[name_color][kernel]
        else:
            marker_color = color_dictionnary[name_color]
        if name == "pearson_correlation":
            name = "Pearson"
        elif name == "MMD":
            name = "cMMD"
        bars.append(
            go.Bar(
                x=alphas,
                y=missing["n"],
                name=name + s3 + s2,
                marker_color=marker_color
            )
        )
    fig = go.Figure(bars)
    fig.update_layout(
        template="ggplot2",
        title=None,
        xaxis_title="<i>&#945;</i>",
        yaxis_title="% of empty sets",
        legend_title="",
        font=dict(size=18),
    )

    fig.write_image(f"images/empty_set_{opt.name}.png", width=1350, height=900)
    fig.write_html(f"empty_set_{opt.name}.html")

    # remove those which didn't select anything


if __name__ == "__main__":
    main()
