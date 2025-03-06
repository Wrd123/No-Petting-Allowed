import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

def load_and_merge_data(main_filepath, gt_filepath, features_filepath):
    """
    Load the main dataset using column names from the features file,
    then merge it with the ground truth table.
    
    Args:
        main_filepath (str): Path to the main dataset CSV file.
        gt_filepath (str): Path to the ground truth CSV file.
        features_filepath (str): Path to the features CSV file containing column metadata.
    
    Returns:
        pd.DataFrame: Merged and cleaned dataset.
    """
    # Check for file existence
    for path, desc in [(main_filepath, "Main data file"), (gt_filepath, "Ground truth file"), 
                       (features_filepath, "Features file")]:
        if not os.path.exists(path):
            logging.error(f"{desc} {path} not found.")
            return pd.DataFrame()

    # Load the features file with the header (it should have columns like "No.", "Name", "Type ", "Description")
    try:
        features_df = pd.read_csv(features_filepath, encoding='cp1252')
    except Exception as e:
        logging.error("Error reading features file: %s", e)
        return pd.DataFrame()
    
    # Extract the actual feature names from the "Name" column.
    if "Name" not in features_df.columns:
        logging.error("Features file does not contain 'Name' column.")
        return pd.DataFrame()
    unsw_columns = features_df["Name"].tolist()
    logging.info("Loaded feature names from features file: %s", unsw_columns)
    
    # Load the main dataset using these column names.
    logging.info("Loading main dataset from %s", main_filepath)
    try:
        df_main = pd.read_csv(main_filepath, header=None, names=unsw_columns, low_memory=False)
    except Exception as e:
        logging.error("Error reading main dataset: %s", e)
        return pd.DataFrame()

    # Load the ground truth data.
    logging.info("Loading ground truth data from %s", gt_filepath)
    try:
        df_gt = pd.read_csv(gt_filepath, low_memory=False)
    except Exception as e:
        logging.error("Error reading ground truth data: %s", e)
        return pd.DataFrame()

    # Debug: Print column names from both datasets.
    logging.info("Main dataset columns after renaming: %s", df_main.columns.tolist())
    logging.info("Ground truth columns: %s", df_gt.columns.tolist())

    # Define the composite key for merging.
        # Define the composite key for merging
    merge_columns_main = ["srcip", "sport", "dstip", "dsport", "proto"]
    merge_columns_gt = ["Source IP", "Source Port", "Destination IP", "Destination Port", "Protocol"]

    # Ensure merge key columns are of the same type (convert to string)
    for col in merge_columns_main:
        df_main[col] = df_main[col].astype(str)
    for col in merge_columns_gt:
        df_gt[col] = df_gt[col].astype(str)

    logging.info("Merging main dataset with ground truth on composite key: %s (main) and %s (gt)",
                 merge_columns_main, merge_columns_gt)
    df_merged = pd.merge(df_main, df_gt, left_on=merge_columns_main, right_on=merge_columns_gt, how='inner')
    logging.info("Merged dataset shape: %s", df_merged.shape)

    # Clean the merged data.
    df_merged.drop_duplicates(inplace=True)
    df_merged.fillna(method='ffill', inplace=True)
    logging.info("Data cleaning complete. Final dataset shape: %s", df_merged.shape)

    return df_merged

def exploratory_data_analysis(df):
    """
    Perform Exploratory Data Analysis (EDA) to generate descriptive statistics and visualizations.
    
    Visualizations include:
        - Time Series Plot (if 'timestamp' and 'traffic_volume' exist)
        - Bar Chart (if 'event_type' exists)
        - Pie Chart (if 'attack_category' exists)
    """
    if df.empty:
        logging.warning("Empty dataset provided to EDA. Skipping analysis.")
        return

    stats = df.describe()
    logging.info("Data Summary:\n%s", stats)

    # Time Series Example (if applicable)
    if 'timestamp' in df.columns and 'traffic_volume' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values('timestamp', inplace=True)
        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['traffic_volume'], label='Traffic Volume')
        plt.xlabel('Time')
        plt.ylabel('Traffic Volume')
        plt.title('Network Traffic Over Time')
        plt.legend()
        plt.tight_layout()
        plt.savefig("time_series_plot.png")
        plt.close()
        logging.info("Time series plot saved as time_series_plot.png")

    # Bar Chart Example (if applicable)
    if 'event_type' in df.columns:
        event_counts = df['event_type'].value_counts()
        plt.figure(figsize=(8, 5))
        event_counts.plot(kind='bar')
        plt.xlabel('Event Type')
        plt.ylabel('Count')
        plt.title('Event Type Frequency')
        plt.tight_layout()
        plt.savefig("bar_chart_event_types.png")
        plt.close()
        logging.info("Bar chart saved as bar_chart_event_types.png")

    # Pie Chart Example (if applicable)
    if 'attack_category' in df.columns:
        attack_counts = df['attack_category'].value_counts()
        plt.figure(figsize=(6, 6))
        attack_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.ylabel('')
        plt.title('Attack Category Distribution')
        plt.tight_layout()
        plt.savefig("pie_chart_attack_category.png")
        plt.close()
        logging.info("Pie chart saved as pie_chart_attack_category.png")
