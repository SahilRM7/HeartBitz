import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
df = pd.read_csv('dataset_heart.csv')

# Define features (X) and target (y)
X = df.drop('num', axis=1)
y = df['num']

# Split the dataset into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the parameter grid for Random Forest
rf_param_grid = {
    "n_estimators": [10, 20, 50, 100],
    "max_depth": [None, 5, 10, 15],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["auto", "sqrt", "log2"],
    "random_state": [12],
}

# Create a Random Forest model
RF = RandomForestClassifier()

# Perform grid search with cross-validation
rf_grid_search = GridSearchCV(RF, rf_param_grid, cv=5, scoring="accuracy")
rf_grid_search.fit(X_train, Y_train)

# Get the best parameters
best_rf_params = rf_grid_search.best_params_
# print("Best Hyperparameters for Random Forest:", best_rf_params)

# Train a Random Forest model with the best parameters
best_RF_model = RandomForestClassifier(**best_rf_params)

# Train a RandomForest model
# model = RandomForestClassifier()
best_RF_model.fit(X_train, Y_train)

# Save the model
with open('model.pkl', 'wb') as file:
    pickle.dump(best_RF_model, file)

# Initialize and fit the scaler
scaler = StandardScaler()
scaler.fit(X)

# Save the scaler to a .pkl file
joblib.dump(scaler, 'scaler.pkl')