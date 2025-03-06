import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

def load_and_merge_data(main_filepath, gt_filepath):
    """
    Load the main dataset and ground truth table, merge them, and perform cleaning.

    Args:
        main_filepath (str): Path to the main dataset CSV file.
        gt_filepath (str): Path to the ground truth CSV file.

    Returns:
        pd.DataFrame: Merged and cleaned dataset.
    """
    # Check if files exist
    if not os.path.exists(main_filepath):
        logging.error(f"Main data file {main_filepath} not found.")
        return pd.DataFrame()

    if not os.path.exists(gt_filepath):
        logging.error(f"Ground truth file {gt_filepath} not found.")
        return pd.DataFrame()

    logging.info("Loading main dataset from %s", main_filepath)
    df_main = pd.read_csv(main_filepath)

    logging.info("Loading ground truth data from %s", gt_filepath)
    df_gt = pd.read_csv(gt_filepath)

    # Merge on a common identifier. Change 'session_id' to whatever column both CSVs share.
    # 'how="inner"' merges only matching rows. Use 'how="left"' if you want all main data rows retained.
    if 'session_id' not in df_main.columns or 'session_id' not in df_gt.columns:
        logging.error("Column 'session_id' not found in one of the files. "
                      "Update the merge key to match your actual dataset schema.")
        return pd.DataFrame()

    logging.info("Merging main dataset with ground truth on 'session_id'...")
    df_merged = pd.merge(df_main, df_gt, on='session_id', how='inner')
    logging.info("Merged dataset shape: %s", df_merged.shape)

    # Clean the merged data
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

    # Time Series Example
    if 'timestamp' in df.columns and 'traffic_volume' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values('timestamp', inplace=True)
        plt.figure(figsize=(10,6))
        plt.plot(df['timestamp'], df['traffic_volume'], label='Traffic Volume')
        plt.xlabel('Time')
        plt.ylabel('Traffic Volume')
        plt.title('Network Traffic Over Time')
        plt.legend()
        plt.tight_layout()
        plt.savefig("time_series_plot.png")
        plt.close()
        logging.info("Time series plot saved as time_series_plot.png")

    # Bar Chart Example
    if 'event_type' in df.columns:
        event_counts = df['event_type'].value_counts()
        plt.figure(figsize=(8,5))
        event_counts.plot(kind='bar')
        plt.xlabel('Event Type')
        plt.ylabel('Count')
        plt.title('Event Type Frequency')
        plt.tight_layout()
        plt.savefig("bar_chart_event_types.png")
        plt.close()
        logging.info("Bar chart saved as bar_chart_event_types.png")

    # Pie Chart Example
    if 'attack_category' in df.columns:
        attack_counts = df['attack_category'].value_counts()
        plt.figure(figsize=(6,6))
        attack_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.ylabel('')
        plt.title('Attack Category Distribution')
        plt.tight_layout()
        plt.savefig("pie_chart_attack_category.png")
        plt.close()
        logging.info("Pie chart saved as pie_chart_attack_category.png")
