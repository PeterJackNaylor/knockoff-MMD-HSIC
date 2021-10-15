import argparse
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from colors import inside_colors, name_mapping, hector_color, mapping_data_name
import os


def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
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
kernel_methods = ["HSIC", "MMD", "MMD_bis"]


def main():
    # Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    # remove those which didn't select anything
    table.loc[table["fdr"] == -1, "fdr"] = 0

    table = table.loc[table["alpha"] == 0.5]
    table = table.loc[table["DATASET"] != 0]
    datasets = np.unique(table["DATASET"])
    kernels = list(np.unique(table["kernel"]))

    if not os.path.exists("images"):
        os.mkdir("images")

    for data in list(datasets):
        table_data = table.loc[table["DATASET"] == data]
        groups = table_data.groupby(["n", "p", "AM", "kernel", "normalise"])

        fig = make_subplots(
            rows=3,
            cols=3,
            shared_xaxes=True,
            shared_yaxes=False,
            vertical_spacing=0.06,
            horizontal_spacing=0.04,
            subplot_titles=titles,
            x_title="",
            y_title="<i>Minimum model size</i>",
        )
        legend = []
        for g_n, group in groups:

            name = g_n[2]
            kernel = g_n[3]
            normalised = g_n[4] == 1
            if normalised:
                continue
            hover_name = name_mapping(name, kernel, normalised)
            if name in kernel_methods:
                hover_name = hover_name + f"({kernel})"
                fill_color = None
            else:
                fill_color = inside_colors[kernel]

            if (name, normalised) in legend:
                display_legend = False
            else:
                display_legend = True
                legend.append((name, normalised))

            n = int(g_n[0])
            p = int(g_n[1])

            size_model = np.array(group["k0"])

            fill_color = hector_color[hover_name]
            boxes = go.Box(
                y=size_model,
                name=hover_name,
                marker_color="black",
                fillcolor=fill_color,
                showlegend=False,
                boxpoints="suspectedoutliers",
                boxmean=True,
                # boxpoints=False,
                marker_size=2,
            )

            fig.add_trace(boxes, row=row_dic[p], col=col_dic[n])
            if display_legend:
                if name == "MMD":
                    hover_name = "MMD(gaussian)"

                elif name == "HSIC":
                    hover_name = "HSIC(gaussian)"
                fill_color = hector_color[hover_name]
                boxes = go.Scatter(
                    x=[None],
                    y=[None],
                    name=name_mapping(name, kernel, normalised),
                    mode="markers",
                    marker_color=fill_color,
                    marker=dict(size=12, line=dict(width=2, color="black")),
                    marker_symbol="square",
                    showlegend=True,
                    marker_size=15,
                )

                fig.add_trace(boxes, row=row_dic[p], col=col_dic[n])
        title = f"Dataset: {mapping_data_name[data]}"
        fig.update_layout(
            template="ggplot2",
            legend_title_text="Association measure",
            title={"text": title, "x": 0.85, "y": 0.88},
            font=dict(size=22),
        )
        for kernel in kernels:
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    legendgroup="group2",
                    legendgrouptitle_text="Kernel",
                    name=kernel.capitalize(),
                    marker_symbol="square",
                    mode="markers",
                    marker=dict(color=inside_colors[kernel], size=10),
                ),
                row=1,
                col=1,
            )

        # fig.layout.annotations[-2]["font"] = {'size': 30}
        fig.layout.annotations[-1]["xshift"] -= 15
        fig.layout.annotations[-1]["font"] = {"size": 22}
        fig.update_xaxes(tickvals=[], ticktext=[])

        fig.update_layout(legend=dict(x=0.75, y=0.95))

        basename = mapping_data_name[data].replace('.', '_')
        fig.write_image(
            f"images/{basename}_minimum_model_size--box_plots.png",
            width=1350,
            height=900,
        )
        fig.write_html(
            f"{basename}_minimum_model_size--box_plots.html"
        )


if __name__ == "__main__":
    main()
