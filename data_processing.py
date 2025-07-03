import os
import yaml
import pandas as pd
from collections import defaultdict

# Root directory containing month folders
data_dir = "data"

# Dictionary to hold lists of data per symbol
symbol_data = defaultdict(list)

# Loop through all month folders like data/2023-10/
for month_folder in os.listdir(data_dir):
    month_path = os.path.join(data_dir, month_folder)
    if os.path.isdir(month_path):
        # Loop through YAML files in the folder
        for file in os.listdir(month_path):
            if file.endswith(".yaml"):
                file_path = os.path.join(month_path, file)
                with open(file_path, 'r') as stream:
                    try:
                        daily_records = yaml.safe_load(stream)
                        for record in daily_records:
                            symbol_data[record['Ticker']].append(record)
                    except yaml.YAMLError as exc:
                        print(f"Error parsing {file_path}: {exc}")

# Output folder for CSV files
output_folder = "processed_data"
os.makedirs(output_folder, exist_ok=True)

# Convert each symbol's data into a DataFrame and save to CSV
for symbol, records in symbol_data.items():
    df = pd.DataFrame(records)
    df.sort_values("date", inplace=True)
    df.to_csv(os.path.join(output_folder, f"{symbol}.csv"), index=False)

print(f"Extraction complete. CSVs saved to: {output_folder}")

# Merge all CSVs into one master file
all_dfs = []
for file in os.listdir(output_folder):
    if file.endswith(".csv") and file != "final_stock_data.csv" and file != "sector_mapping.csv":
        df = pd.read_csv(os.path.join(output_folder, file))
        all_dfs.append(df)

df_final = pd.concat(all_dfs, ignore_index=True)
df_final.to_csv(os.path.join(output_folder, "final_stock_data.csv"), index=False)
print("Merged all individual stock files into final_stock_data.csv")

# Manually defined sector mapping (based on Nifty 50 composition)
sector_dict = {
    "SBIN": "Banking",
    "ICICIBANK": "Banking",
    "AXISBANK": "Banking",
    "KOTAKBANK": "Banking",
    "HDFCBANK": "Banking",
    "BAJAJFINSV": "Financials",
    "BAJFINANCE": "Financials",
    "HDFCLIFE": "Insurance",
    "SBILIFE": "Insurance",
    "ITC": "FMCG",
    "HINDUNILVR": "FMCG",
    "NESTLEIND": "FMCG",
    "ULTRACEMCO": "Cement",
    "GRASIM": "Cement",
    "TATASTEEL": "Metals",
    "JSWSTEEL": "Metals",
    "HINDALCO": "Metals",
    "ONGC": "Energy",
    "COALINDIA": "Energy",
    "NTPC": "Energy",
    "POWERGRID": "Energy",
    "RELIANCE": "Energy",
    "TATAMOTORS": "Auto",
    "EICHERMOT": "Auto",
    "HEROMOTOCO": "Auto",
    "BAJAJ-AUTO": "Auto",
    "CIPLA": "Pharma",
    "SUNPHARMA": "Pharma",
    "DRREDDY": "Pharma",
    "INFY": "IT",
    "TCS": "IT",
    "WIPRO": "IT",
    "TECHM": "IT",
    "HCLTECH": "IT",
    "ASIANPAINT": "Consumer",
    "BRITANNIA": "Consumer",
    "TATACONSUM": "Consumer",
    "ADANIPORTS": "Infra",
    "ADANIENT": "Conglomerate",
    "LT": "Infra",
    "DIVISLAB": "Pharma",
    "SHRIRAMFIN": "Financials",
    "INDUSINDBK": "Banking",
    "BPCL": "Energy",
    "APOLLOHOSP": "Healthcare",
    "TRENT": "Retail",
    "BEL": "Defense",
}

sector_df = pd.DataFrame(list(sector_dict.items()), columns=["Ticker", "Sector"])
sector_df.to_csv(os.path.join(output_folder, "sector_mapping.csv"), index=False)
print("Sector mapping file saved to sector_mapping.csv")
