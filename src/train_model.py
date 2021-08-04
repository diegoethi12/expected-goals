import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, KFold


from src import DATA_PATH, MODEL_PATH


shots = pd.read_pickle(DATA_PATH / 'open_shots.pkl')

# Config
NUMERICAL_FEATURES = ['distance', 'angle']
CATEGORICAL_FEATURES = ['play_pattern', 'shot_body_part', 'shot_technique']
FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
TARGET = 'goal'
RS = 12

# Train test split
x = shots[FEATURES]
y = shots[TARGET]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=RS)

numerical_transformer = Pipeline(steps=[
    ('standard_scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('one_hot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('numeric', numerical_transformer, NUMERICAL_FEATURES),
    ('categorical', categorical_transformer, CATEGORICAL_FEATURES)
]
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier())
])

# Training routine
param_grid = {
    'classifier__max_depth': [2, 3, 5],
    'classifier__learning_rate': [0.05, 0.1, 0.15],
    'classifier__n_estimators': [50, 100, 150],
    'classifier__random_state': [RS]
}

grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='roc_auc',
    refit=True,
    cv=KFold(n_splits=5),
    n_jobs=-1,
    verbose=2
)

grid.fit(x_train, y_train)

results = pd.DataFrame(grid.cv_results_)
results.sort_values('rank_test_score')[['mean_fit_time', 'mean_test_score', 'std_test_score']]

best_model = grid.best_estimator_

# Test prediction
y_pred_score = best_model.predict_proba(x_test)

# Save model
joblib.dump(best_model, MODEL_PATH / 'model.joblib')
