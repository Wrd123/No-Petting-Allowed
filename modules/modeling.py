import logging
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def train_predictive_model(df_train, test_data=None):
    # Define your required columns, e.g., ['sbytes', 'dbytes', 'spkts', 'Label']
    required_columns = ['sbytes', 'dbytes', 'spkts', 'Label']
    for col in required_columns:
        if col not in df_train.columns:
            logging.error("Column '%s' is missing from the training set.", col)
            return None

    # Extract features and target for training
    X_train = df_train[['sbytes', 'dbytes', 'spkts']]
    y_train = df_train['Label']
    
    # If you have a separate testing set, extract features and target similarly
    if test_data is not None:
        for col in required_columns:
            if col not in test_data.columns:
                logging.error("Column '%s' is missing from the testing set.", col)
                return None
        X_test = test_data[['sbytes', 'dbytes', 'spkts']]
        y_test = test_data['Label']
    else:
        X_test = y_test = None

    # Split data, train the model, and evaluate. For example, using a Random Forest:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    import numpy as np

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logging.info("Model training complete.")

    if X_test is not None:
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        logging.info("Model Accuracy: %.2f%%", acc * 100)
        # Optionally, compute and log confusion matrix, classification report, etc.
        cm = confusion_matrix(y_test, y_pred)
        logging.info("Confusion Matrix:\n%s", cm)
        cv_scores = np.mean([accuracy_score(y_test, model.predict(X_test))])
        logging.info("Average CV Score: %.2f%%", cv_scores * 100)

    return model