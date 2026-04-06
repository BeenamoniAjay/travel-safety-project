import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load dataset
data = pd.read_csv("data/data.csv")

# Features and target
X = data[['crime','disaster','health']]
y = data['danger']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully!")