#!/usr/bin/env python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

def load_npz(path):
    data = np.load(path)
    X = data['X']
    y = data['Y']
    return X,y

X_train, y_train = load_npz("${Xy_train}")
X_test, y_test = load_npz("${Xy_test}")

df = pd.read_csv("${FEATURES}")
selected_features = [ str(x).split(',') for x in df.features ]

clf = RandomForestClassifier()

param_grid = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'log2'],
    'max_depth' : [4,6,8],
    'criterion' :['gini', 'entropy']
}

accuracies = []

for alpha, features in zip(df.alpha, selected_features):
    if features == ['nan']:
        accuracies.append(None)
        continue

    features = [ int(x) for x in features ]
    X_train_alpha = X_train[:,features]
    X_test_alpha = X_test[:,features]

    cv_clf = GridSearchCV(clf, param_grid)
    cv_clf.fit(X_train_alpha, y_train)

    y_pred = cv_clf.predict(X_test_alpha)
    
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

data_out = {'DATASET': df.DATASET,
            'fold': df.fold,
            'AM': df.AM,
            'alpha': df.alpha,
            'features': df.features,
            'accuracy': accuracies}

df_out = pd.DataFrame(data_out) 
df_out.to_csv("accuracy.csv", index=False)
