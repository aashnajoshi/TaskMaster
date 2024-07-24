import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import numpy as np

# Load dataset
df = pd.read_csv('customer_booking.csv', encoding='ISO-8859-1')

# Basic statistics
print(df.info())
print(df.describe())
print(df.head())

# Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)  # or df.dropna()

# Convert categorical variables into dummy/indicator variables
categorical_columns = ['sales_channel', 'trip_type', 'flight_day', 'route', 'booking_origin']
df = pd.get_dummies(df, columns=categorical_columns)

# Feature engineering (if applicable)
# Here, 'flight_hour' and 'flight_duration' are numeric already, so no need to create new features

# Define features (X) and target (y)
X = df.drop('booking_complete', axis=1)
y = df['booking_complete']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Cross-validation
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation scores: {cv_scores}")

# Evaluation
print(classification_report(y_test, y_pred))
roc_auc = roc_auc_score(y_test, y_proba)
print(f"ROC-AUC: {roc_auc}")

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
fig, ax = plt.subplots()
ax.plot(fpr, tpr, label=f'ROC Curve (area = {roc_auc:.2f})')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.legend()
fig.savefig('roc_curve.png')

# Feature importance
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(range(X.shape[1]), importances[indices], align='center')
ax.set_xticks(range(X.shape[1]))
ax.set_xticklabels(X.columns[indices], rotation=90)
ax.set_title('Feature Importances')
fig.savefig('feature_importances.png')