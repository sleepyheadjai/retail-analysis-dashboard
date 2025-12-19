# Retail Analysis Dashboard
An interactive retail analytics dashboard built using Python and Streamlit to analyze sales, revenue, and inventory data.
Live application:  
https://retail-analysis-dashboard-8re74ennan5eydvgmc6n2y.streamlit.app/

## Overview
This project focuses on analyzing retail performance through an interactive dashboard. It helps understand sales trends, product performance, and inventory behavior across different stores and suppliers. A sample dataset covering the years 2024–2025 is preloaded for demonstration and analysis.

## Tech Stack
Python, Streamlit, Pandas, NumPy, Matplotlib, Plotly, Git, GitHub

## Features
- Interactive sidebar filters (Store and Date mandatory; Supplier and Product optional)
- Key performance indicators (Total Revenue, Total Transactions, Average Order Value, Reorder Rate)
- Visual analysis (Revenue trends, Product-wise revenue distribution, Low-stock and reorder analysis)
- Filtered dataset preview
- Option to download filtered data as a CSV file

## Project Structure

```
retail-analysis-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│ └── retail_dataset.csv
└── notebooks/
└── retail_analysis.ipynb
```

## Run Locally

```
git clone https://github.com/sleepyheadjai/retail-analysis-dashboard.git

cd retail-analysis-dashboard
pip install -r requirements.txt
streamlit run app.py
```
