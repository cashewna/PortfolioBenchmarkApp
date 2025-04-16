import pandas as pd
import glob
import os

def calculate_correlation(folder_path: str) -> pd.DataFrame:
    """
    Calculate correlation matrix from all CSV files in a folder, each containing one asset's data.
    
    Args:
        folder_path (str): Path to folder containing CSV files
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    # Get all CSV files in the folder
    file_paths = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not file_paths:
        raise ValueError(f"No CSV files found in directory: {folder_path}")
    
    # Read all files and store in a dictionary
    assets = {}
    for file_path in file_paths:
        asset_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            assets[asset_name] = pd.read_csv(file_path, parse_dates=['Date'])
        except Exception as e:
            print(f"Warning: Could not read file {file_path}. Error: {e}")
            continue
    
    if not assets:
        raise ValueError("No valid CSV files could be read")
    
    # Merge all dataframes on date
    merged = None
    for asset_name, df in assets.items():
        if merged is None:
            merged = df[['Date', 'PX_LAST']].copy()
            merged.rename(columns={'PX_LAST': asset_name}, inplace=True)
        else:
            temp = df[['Date', 'PX_LAST']].copy()
            temp.rename(columns={'PX_LAST': asset_name}, inplace=True)
            merged = pd.merge(merged, temp, on='Date', how='inner')
    
    # Calculate correlation matrix
    price_columns = [col for col in merged.columns if col != 'Date']
    corr_matrix = merged[price_columns].corr()
    
    return corr_matrix
if __name__ == "__main__":
    folder_path = "./src/main/resources"

    try:
        correlation = calculate_correlation(folder_path)
        print(correlation)
    except Exception as e:
        print(f"An error occurred: {e}")