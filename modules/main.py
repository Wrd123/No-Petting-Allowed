import logging
import pandas as pd
from modeling import train_predictive_model
from dashboard import build_dashboard
from security import apply_security_measures

def main():
    # Apply security measures (if needed)
    security_config = apply_security_measures()

    # Define file paths for the training and testing sets.
    training_set_path = '../data/UNSW_NB15_training-set.csv'
    testing_set_path  = '../data/UNSW_NB15_testing-set.csv'
    
    # Load the training set and testing set.
    try:
        df_train = pd.read_csv(training_set_path, low_memory=False)
        df_test  = pd.read_csv(testing_set_path, low_memory=False)
    except Exception as e:
        logging.error("Error loading training or testing set: %s", e)
        return

    logging.info("Training set shape: %s", df_train.shape)
    logging.info("Testing set shape: %s", df_test.shape)
    
    # Now, pass these dataframes to your model training function.
    # If your current train_predictive_model function expects a single dataframe,
    # you might update it to accept training and testing data separately.
    model = train_predictive_model(df_train, test_data=df_test)
    if model is None:
        logging.error("Model training failed. Exiting.")
        return

    # Optionally, you can build the dashboard based on the training set (or combined data)
    app = build_dashboard(df_train)
    
    # Run the Dash app (for external access, you might use host='0.0.0.0')
    app.run_server(debug=True, host='0.0.0.0', port=8050)

if __name__ == '__main__':
    main()
