# Import required libraries
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Dashboard title
st.title("Satellite-Based Forest Cover Analysis Dashboard")

# Project description
st.write("""
This dashboard demonstrates forest cover classification
using geographical and environmental features.
""")


# Import os to handle file paths correctly
import os

# Get the current file location
current_dir = os.path.dirname(__file__)

# Build the correct path to the dataset
data_path = os.path.join(current_dir, "..", "data", "covtype.csv")

# Load dataset

df = pd.read_csv(data_path).sample(50000, random_state=42)

# Display dataset shape
st.subheader("Dataset Information")

st.write("Rows and Columns:", df.shape)

# Display first rows
st.subheader("Dataset Preview")

st.dataframe(df.head())

# Forest cover distribution
st.subheader("Forest Cover Type Distribution")

cover_counts = df['Cover_Type'].value_counts().sort_index()

fig1, ax1 = plt.subplots()

cover_counts.plot(kind='bar', ax=ax1)

ax1.set_title("Forest Cover Type Distribution")
ax1.set_xlabel("Cover Type")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# Elevation distribution
st.subheader("Elevation Distribution")

fig2, ax2 = plt.subplots()

ax2.hist(df['Elevation'], bins=30)

ax2.set_title("Elevation Distribution")
ax2.set_xlabel("Elevation")
ax2.set_ylabel("Frequency")

st.pyplot(fig2)

# Machine Learning Section
st.subheader("Machine Learning Model")

# Features and target
X = df.drop('Cover_Type', axis=1)
y = df['Cover_Type']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

# Display accuracy
st.success(f"Model Accuracy: {accuracy:.2f}")

# Feature Importance
st.subheader("Top Feature Importance")

importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

top_features = importance_df.head(10)

fig3, ax3 = plt.subplots()

ax3.barh(
    top_features['Feature'],
    top_features['Importance']
)

ax3.set_title("Top 10 Important Features")
ax3.set_xlabel("Importance")

ax3.invert_yaxis()

st.pyplot(fig3)

# Final summary
st.subheader("Project Summary")

st.write("""
This project demonstrates the use of machine learning
and GIS-related environmental variables for forest
cover classification and environmental analysis.
""")
