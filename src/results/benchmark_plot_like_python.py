import os
import argparse
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from colors import (
    color_dictionnary_fdr,
    color_dictionnary_fdr_keys,
    name_mapping_fdr,
    mapping_data_name,
)


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

titles = tuple(
    f"<b> {text} </b>" if text != "" else text
    for text in [
        "n = 100; p = 100",
        "n = 500; p = 100",
        "",
        "n = 100; p = 500",
        "n = 500; p = 500",
        "",
        "n = 100; p = 5000",
        "n = 500; p = 5000",
        "n = 1000; p = 5000",
    ]
)

tikz_y = [0, 0.25, 0.5, 0.75, 1.0]
tikz_text_y = ["0.00", "0.25", "0.50", "0.75", "1.00"]

tikz_x = [0.25, 0.5, 0.75]
tikz_text_x = ["0.25", "0.50", "0.75"]

id_ = [i / 100 for i in range(0, 105, 5)]


def main():
    # Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    # set to 0 those which didn't select anything
    table.loc[table["fdr"] == -1, "fdr"] = 0
    table = table.dropna()
    table = table.loc[table["DATASET"] != 0]
    datasets = np.unique(table["DATASET"])

    if not os.path.exists("images"):
        os.mkdir("images")

    for data in list(datasets):
        table_data = table.loc[table["DATASET"] == data]

        groups = table_data.groupby(["n", "p", "AM", "normalise", "kernel"])
        fig = make_subplots(
            rows=3,
            cols=3,
            shared_xaxes=True,
            shared_yaxes=True,
            vertical_spacing=0.06,
            horizontal_spacing=0.04,
            subplot_titles=titles,
            x_title="<i>&#945;</i>",  # , 'font': {'size': 0}},
            y_title="<i>FDR</i>",
        )
        legend = {el: True for el in color_dictionnary_fdr_keys}

        for g_n, group in groups:

            n = int(g_n[0])
            p = int(g_n[1])
            name = g_n[2]
            kernel = g_n[4]
            normalised = g_n[3] == 1
            only_kernel = opt.kernels == 1

            if only_kernel:
                if name not in ["HSIC", "MMD"]:
                    continue
            else:
                if name in ["HSIC", "MMD"] and kernel != "gaussian":
                    continue

            alpha_group = group.groupby(["alpha"])
            mean = alpha_group.mean()
            sample_number = alpha_group.count()
            std = alpha_group.std()

            x = mean.index.sort_values()
            y = mean.loc[x, "fdr"]
            std = std.loc[x, "fdr"]
            n_samples = sample_number.loc[x, "fdr"]
            err = 1.96 * std / (n_samples) ** 0.5
            curve_name = name_mapping_fdr(name, kernel, normalised)

            curve = go.Scatter(
                x=x,
                y=y,
                name=curve_name,
                error_y=dict(array=err),
                marker=dict(
                    color=color_dictionnary_fdr(
                        name, kernel, normalised, only_kernel=only_kernel
                    )
                ),
                showlegend=legend[curve_name],
            )

            if legend[curve_name]:
                legend[curve_name] = False

            fig.add_trace(curve, row=row_dic[p], col=col_dic[n])
            fig.add_trace(
                go.Scatter(
                    x=id_,
                    y=id_,
                    name="",
                    marker={"color": "rgb(0, 0, 0)"},
                    line=dict(width=0.5),
                    showlegend=False,
                ),
                row=row_dic[p],
                col=col_dic[n],
            )
        title = f"Dataset: {mapping_data_name[data]}"
        fig.update_layout(
            template="ggplot2",
            legend_title_text="Association measure:",
            title={"text": title, "x": 0.85, "y": 0.88},
            font=dict(size=22),
        )

        fig.layout.annotations[-2]["font"] = {"size": 30}
        fig.layout.annotations[-1]["xshift"] -= 15
        fig.layout.annotations[-1]["font"] = {"size": 22}
        fig.update_yaxes(range=(0, 1.0), tickvals=tikz_y, ticktext=tikz_text_y)
        fig.update_xaxes(range=(0, 1.0), tickvals=tikz_x, ticktext=tikz_text_x)
        fig.update_layout(legend=dict(x=0.75, y=0.95))

        model_name = mapping_data_name[data].replace('.', '_')
        basename = f"{model_name}_fdr_controls_{opt.name}"
        fig.write_image(
            f"images/{basename}.png",
            width=1350,
            height=900,
        )
        fig.write_html(
            f"{basename}.html"
        )


if __name__ == "__main__":
    main()
