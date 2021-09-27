
import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from colors import color_dictionnary, positions

def options():
    # options
    parser = argparse.ArgumentParser(description="Knock off run")
    parser.add_argument("--csv_file", type=str)
    args = parser.parse_args()

    return args

row_dic = {100: 1, 500: 2, 5000: 3}
col_dic = {100: 1, 500: 2, 1000: 3}





titles = tuple(f"<b> {text} </b>" if text != "" else text for text in \
        ["n = 100; p = 100", "n = 500; p = 100",  "",
        "n = 100; p = 500", "n = 500; p = 500",  "",
        "n = 100; p = 5000", "n = 500; p = 5000",  "n = 1000; p = 5000"])


tikz_y = [0, 0.25, 0.5, 0.75, 1.0]
tikz_text_y = ["0.00", "0.25", "0.50", "0.75", "1.00"]



def main():
    ## Load data
    opt = options()
    table = pd.read_csv(opt.csv_file)
    # remove those which didn't select anything
    table.loc[table["fdr"] == -1, "fdr"] = 0

    table = table.loc[table["alpha"] == 0.5]
    table = table.loc[table['DATASET'] != 0]
    datasets = np.unique(table['DATASET'])

    for data in list(datasets):
        table_data = table.loc[table['DATASET'] == data]
        groups = table_data.groupby(["n", "p", "AM"])

        fig = make_subplots(rows=3, cols=3,
                            shared_xaxes=True,
                            shared_yaxes=False,
                            vertical_spacing=0.06,
                            horizontal_spacing=0.04,
                            subplot_titles=titles,
                            x_title="",#, 'font': {'size': 0}},
                            y_title='<i>Minimum model size</i>')
        legend = {el: True for el in color_dictionnary.keys()}

        for g_n, group in groups:
            n = int(g_n[0])
            p = int(g_n[1])

            size_model = np.array(group["k0"])

            boxes = go.Box(
                        y=size_model,
                        name=f"{g_n[2]}",
                        marker_color=color_dictionnary[g_n[2]],
                        showlegend=legend[g_n[2]],
                        boxmean=True,
                        boxpoints=False
                    )

            if legend[g_n[2]]:
                legend[g_n[2]] = False
            fig.add_trace(boxes, row=row_dic[p], col=col_dic[n])
            
        fig.update_layout(template="ggplot2", legend_title_text='Algorithm',
                    title={
                        'text': f"Dataset: {data}".replace("_", " "),
                        'x': 0.85,
                        'y': 0.88},
                    font=dict(
                        size=22
                    ))
        
        # fig.layout.annotations[-2]["font"] = {'size': 30}
        fig.layout.annotations[-1]["xshift"] -= 15
        fig.layout.annotations[-1]["font"] = {'size': 22}
        fig.update_xaxes(tickvals=[], ticktext=[])

        fig.update_layout(legend=dict(
            x=0.75,
            y=0.80
        ))
        fig.write_html(f"{data}_minimum_model_size--box_plots.html")

if __name__ == "__main__":
    main()
