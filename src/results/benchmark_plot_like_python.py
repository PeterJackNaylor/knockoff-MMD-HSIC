
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

titles = tuple(f"<b> {text} </b>" if text != "" else text for text in \
        ["n = 100; p = 100", "n = 500; p = 100",  "",
        "n = 100; p = 500", "n = 500; p = 500",  "",
        "n = 100; p = 5000", "n = 500; p = 5000",  "n = 1000; p = 5000"])

tikz_y = [0, 0.25, 0.5, 0.75, 1.0]
tikz_text_y = ["0.00", "0.25", "0.50", "0.75", "1.00"]

tikz_x = [0.25, 0.5, 0.75]
tikz_text_x = ["0.25", "0.50", "0.75"]

id_ = [i / 100 for i in range(0, 105, 5)]

def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    # remove those which didn't select anything
    table.loc[table["fdr"] == -1, "fdr"] = 0
    table = table.loc[table['DATASET'] != 0]
    datasets = np.unique(table['DATASET'])
    for data in list(datasets):
        table_data = table.loc[table['DATASET'] == data]
        groups = table_data.groupby(["n", "p", "AM"])

        fig = make_subplots(rows=3, cols=3,
                            shared_xaxes=True,
                            shared_yaxes=True,
                            vertical_spacing=0.06,
                            horizontal_spacing=0.04,
                            subplot_titles=titles,
                            x_title="<i>&#945;</i>",#, 'font': {'size': 0}},
                            y_title='<i>FDR</i>')
        legend = {"MMD": True,
                    "TR": True,
                    "HSIC": True,
                    "pearson_correlation": True,
                    "PC": True,
                    "DC": True}
        for g_n, group in groups:
            
            alpha_group = group.groupby(['alpha'])
            mean = alpha_group.mean()
            sample_number = alpha_group.count()
            std = alpha_group.std()
            # import pdb; pdb.set_trace()
            n = int(g_n[0])
            p = int(g_n[1])

            x = mean.index.sort_values()
            y = mean.loc[x, "fdr"]
            err = 1.96 * std.loc[x, "fdr"] / (sample_number.loc[x, "fdr"]) ** 0.5
            curve = go.Scatter(
                x=x,
                y=y,
                name=f"{g_n[2]}",
                error_y=dict(
                    array=err),
                marker=dict(
                    color=colors[g_n[2]]
                ),
                showlegend=legend[g_n[2]])
            if legend[g_n[2]]:
                legend[g_n[2]] = False
            fig.add_trace(curve, row=row_dic[p], col=col_dic[n])
            fig.add_trace(go.Scatter(
                            x=id_,
                            y=id_,
                            name="",
                            marker={
                                "color": "rgb(0, 0, 0)"
                            },
                            line=dict(width=0.5),
                            showlegend=False
                        ),
                        row=row_dic[p], col=col_dic[n])
        fig.update_layout(template="ggplot2", legend_title_text='Algorithm',
                    title={
                        'text': f"Dataset: {data}".replace("_", " "),
                        'x': 0.85,
                        'y': 0.88},
                    font=dict(
                        size=22
                    ))
        
        fig.layout.annotations[-2]["font"] = {'size': 30}
        fig.layout.annotations[-1]["xshift"] -= 15
        fig.layout.annotations[-1]["font"] = {'size': 22}
        fig.update_yaxes(range=(0, 1.0), tickvals=tikz_y, ticktext=tikz_text_y)
        fig.update_xaxes(range=(0, 1.0), tickvals=tikz_x, ticktext=tikz_text_x)
        fig.update_layout(legend=dict(
            x=0.75,
            y=0.80
        ))
        fig.write_html(f"{data}_fdr_controls")

if __name__ == "__main__":
    main()
