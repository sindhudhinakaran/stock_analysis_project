# 📊 Nifty 50 Stock Analysis — Data Pipeline and Visualization

## Overview

This project automates the transformation of raw YAML-based daily stock data of Nifty 50 companies into a structured format, maps each stock to its sector, and provides an interactive dashboard for in-depth financial analysis and insights.

---

## Project Workflow

1. **Data Extraction and Aggregation:**  
   The `data_processing.py` script loops through monthly folders (e.g., `data/2023-10/`) containing `.yaml` files, extracts daily stock information, and creates individual CSV files per stock.

2. **Data Merging:**  
   All individual stock CSVs are merged into a master file named `final_stock_data.csv`, which serves as the primary input for visualization.

3. **Sector Mapping:**  
   A predefined dictionary maps stock tickers to sectors (e.g., Banking, FMCG, Pharma), and this is saved as `sector_mapping.csv` for use in sector-wise analysis.

4. **Interactive Visualization:**  
   Built with **Streamlit**, the dashboard enables filtering by stock and month. It includes multiple financial visualizations such as volatility, cumulative return trends, sector performance, correlation heatmaps, and monthly gainers/losers.

---

## Technologies

- **Python 3.9+**  
- **Data Processing:** `pandas`, `yaml`, `os`  
- **Visualization:** `streamlit`, `plotly`, `matplotlib`, `seaborn`  
- **File Formats:** `.yaml`, `.csv`

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nifty50-stock-analysis.git
cd nifty50-stock-analysis
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Organize Input Data

Ensure your daily YAML files are placed in folders named by month, like:

```
data/
  └── 2023-10/
        ├── 2023-10-01.yaml
        ├── 2023-10-02.yaml
  └── 2023-11/
        ├── 2023-11-01.yaml
```

---

## Running the Project

### 🛠 Data Processing

```bash
python data_processing.py
```

- Creates one CSV per stock in `processed_data/`
- Merges all into `final_stock_data.csv`
- Saves `sector_mapping.csv`

### 📈 Launch Dashboard

```bash
streamlit run visualization_streamlit.py
```

Use the **sidebar filters** to choose stocks and months for interactive exploration.

---

## Dashboard Features

### 1. **Top 10 Most Volatile Stocks**
- Measures risk using standard deviation of daily returns
- Bar chart of top 10 stocks by volatility

### 2. **Cumulative Return Over Time**
- Computes `(1 + daily_return).cumprod()` for each stock
- Line chart of top 5 performing stocks by final cumulative return

### 3. **Sector-wise Average Return**
- Merges sector info and computes final cumulative return per ticker
- Averages those per sector
- Bar chart shows which sectors performed best

### 4. **Stock Price Correlation Heatmap**
- Pivot close prices by date/ticker
- Calculate daily percentage change, then correlation
- Heatmap shows co-movement between stocks

### 5. **Top 5 Monthly Gainers and Losers**
- For each month, calculates percent return from the start to end of month
- Shows top 5 gainers and top 5 losers with bar charts

---

## File Structure

```
.
├── data/                          # Raw input YAML files (monthly folders)
├── processed_data/               # Output CSVs
│   ├── final_stock_data.csv      # Merged stock data
│   ├── sector_mapping.csv        # Manual sector assignment
│   └── *.csv                     # Individual stock data files
├── data_processing.py            # Extracts, merges, maps sector
├── visualization_streamlit.py   # Streamlit dashboard
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## Future Improvements

- Support automatic sector detection from online APIs  
- Deploy Streamlit app to cloud (e.g., Streamlit Cloud, Azure)  
- Add advanced technical indicators (e.g., RSI, SMA, Bollinger Bands)  
- Add export/download feature in dashboard  
- Connect to PostgreSQL/SQL for scalable storage and querying

---

## Contact

For suggestions, contributions, or questions, contact:  
📧 dhinakaransindhu96@gmail.com