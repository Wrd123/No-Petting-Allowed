import logging
from security import apply_security_measures
from data_processing import load_and_clean_data, exploratory_data_analysis
from modeling import train_predictive_model
from dashboard import build_dashboard

def main():
    """
    Main function to orchestrate the cybersecurity analytics platform:
        1. Apply security measures.
        2. Load and clean the dataset.
        3. Perform exploratory data analysis.
        4. Train a predictive model.
        5. Launch the interactive dashboard.
    """
    # Apply security measures (placeholders for TLS, encryption, RBAC, etc.)
    apply_security_measures()
    
    # Data Ingestion: Update the path to your actual dataset file
    dataset_path = '../data/UNSW-NB15_1.csv'
    df = load_and_clean_data(dataset_path)
    
    if df.empty:
        logging.error("No data loaded. Exiting program.")
        return
    
    # Perform Exploratory Data Analysis (EDA)
    exploratory_data_analysis(df)
    
    # Train a predictive model (if the necessary features exist)
    model = train_predictive_model(df)
    if model is None:
        logging.error("Model training failed. Exiting predictive module.")
    
    # Build and run the interactive dashboard
    app = build_dashboard(df)
    app.run_server(debug=True)
    
if __name__ == '__main__':
    main()
