#!/usr/bin/env python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV


def load_npz(path):
    data = np.load(path)
    X = data["X"]
    y = data["Y"]
    return X, y


def quality_scores(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)

    return {
        "accuracy": accuracy,
        "sensitivity": sensitivity,
        "specificity": specificity,
    }


X_train, y_train = load_npz("${Xy_train}")
X_test, y_test = load_npz("${Xy_test}")

df = pd.read_csv("${FEATURES}")
selected_features = [str(x).split(",") for x in df.features]

clf = RandomForestClassifier()

param_grid = {
    "n_estimators": [200, 500],
    "max_features": ["auto", "log2"],
    "max_depth": [4, 6, 8],
    "criterion": ["gini", "entropy"],
}

scores = []

for alpha, features in zip(df.alpha, selected_features):
    if features == ["nan"]:
        s = {"accuracy": None, "sensitivity": None, "specificity": None}
        scores.append(s)
        continue

    features = [int(x) for x in features]
    X_train_alpha = X_train[:, features]
    X_test_alpha = X_test[:, features]

    cv_clf = GridSearchCV(clf, param_grid)
    cv_clf.fit(X_train_alpha, y_train)

    y_pred = cv_clf.predict(X_test_alpha)

    score = quality_scores(y_test, y_pred)
    scores.append(score)

data_out = {
    "DATASET": df.DATASET,
    "fold": df.fold,
    "AM": df.AM,
    "alpha": df.alpha,
    "features": df.features,
    "accuracy": [x["accuracy"] for x in scores],
    "sensitivity": [x["sensitivity"] for x in scores],
    "specificity": [x["specificity"] for x in scores],
}


df_out = pd.DataFrame(data_out)
df_out.to_csv("accuracy.csv", index=False)
