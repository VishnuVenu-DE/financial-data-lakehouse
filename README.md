# financial-data-lakehouse
Stock/Crypto data pipeline built using Azure Data Factory, Data Lake, Databricks &amp; Delta Lake


# Financial Data Lakehouse

This project aims to build a modern data pipeline using Azure tools to ingest, process, and analyze stock or cryptocurrency price data.

Tools: Azure Data Factory, Data Lake Gen2, Databricks, Delta Lake


## 📊 Data Source
Data is fetched from [Alpha Vantage](https://www.alphavantage.co) using their free stock API.  
We can collect daily stock prices for symbols like AAPL, MSFT, TSLA.

Sample: `data/raw_sample.csv`