from scipy.stats import kendalltau, spearmanr


def tr(X, Y):
    tau = kendalltau(X, Y).correlation
    rho = spearmanr(X, b=Y).correlation
    return  3 * tau  - 2 * rho

if __name__ == "__main__":
    x, y = [1,2,3,4,5], [5,6,7,8,7]
    print("rho: ", spearmanr(x, y).correlation)
    print("tau: ", kendalltau(x, y).correlation)
    print(f"{tr(x,y)=}")
