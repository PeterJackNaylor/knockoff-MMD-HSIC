import numpy as np
import pandas as pd
import plotly.express as px

rep = 200
p = 5000


def score(S, array):
    n = len(array)
    for i in range(len(S), n, 1):
        if set(S).issubset(array[:i]):
            break
    return i + 1


def main():
    scores = []
    for i in range(rep):
        l1 = list(range(p))
        np.random.shuffle(l1)
        scores.append(score(list(range(10)), l1))

    df = pd.DataFrame(scores)
    df["categorie"] = "random"
    fig = px.box(df, x="categorie", y=0, points="all")
    fig.show()

if __name__ == "__main__":
    main()
