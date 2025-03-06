import logging
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def train_predictive_model(df):
    """
    Train a predictive model using a Random Forest classifier to detect malicious events.
    
    Assumptions:
        - The dataset contains features (e.g., 'feature1', 'feature2', 'feature3') and a target column 'label'
          that indicates if an event is malicious (1) or benign (0).
    
    Args:
        df (pd.DataFrame): Cleaned dataset.
        
    Returns:
        model (RandomForestClassifier): Trained model or None if training cannot proceed.
    """
    # Define required columns – update these based on your dataset
    required_columns = ['feature1', 'feature2', 'feature3', 'label']
    for col in required_columns:
        if col not in df.columns:
            logging.error("Column '%s' is missing from dataset.", col)
            return None
    
    # Select features (X) and target (y)
    X = df[['feature1', 'feature2', 'feature3']]
    y = df['label']
    
    # Split the data into training and testing sets (80/20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logging.info("Data split into training and testing sets.")
    
    # Initialize and train the Random Forest classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logging.info("Model training complete.")
    
    # Evaluate model performance on the test set
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info("Model Accuracy: %.2f%%", acc * 100)
    
    report = classification_report(y_test, y_pred)
    logging.info("Classification Report:\n%s", report)
    
    cm = confusion_matrix(y_test, y_pred)
    logging.info("Confusion Matrix:\n%s", cm)
    
    # Perform 5-fold cross-validation and log the scores
    cv_scores = cross_val_score(model, X, y, cv=5)
    logging.info("Cross-validation scores: %s", cv_scores)
    logging.info("Average CV Score: %.2f%%", np.mean(cv_scores) * 100)
    
    return model
