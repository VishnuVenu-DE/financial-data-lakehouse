# Day 2 – Bronze Layer Data Ingestion

##  Objective
Build a data ingestion pipeline to fetch real-time data from an API and store it in the Bronze layer of ADLS.

---

## Data Source
- CoinGecko API (public REST API)
- No authentication required
- Provides real-time cryptocurrency market data

---

##  Implementation

### 1. API Ingestion
- Used Python `requests` to fetch top cryptocurrencies
- Handled API response validation (status code check)

### 2. Raw Data Storage
- Stored API response as raw JSON in ADLS
- Used `dbutils.fs.put()` to preserve original structure

### 3. Partitioning Strategy
Data stored using ingestion date:

/bronze/crypto/ingestion_date=YYYY-MM-DD/raw_data.json

This ensures:
- Scalability
- Easier querying in later stages
- Organized data layout

---

##  Reusable Configuration (Important Improvement)

### Problem
- ADLS access (OAuth config) had to be repeated in every notebook

### Solution
- Created reusable configuration module: common_scripts/common_funtions.py

### Benefit
- Eliminates duplication
- Centralized configuration
- Cleaner and maintainable code

### Design Decision: Notebook vs Import
- Option 1: dbutils.notebook.run()
    - Executes another notebook as a separate job
    - Useful for orchestration
    - Does NOT share variables
- Option 2: Import as Python module (Chosen Approach)
    - Shares execution context
    - Cleaner structure
    - Better for reusable logic

Used Python module import for configuration instead of notebook chaining.


### Design Decision: Raw vs Spark Write
- Option 1: dbutils.fs.put() (Chosen)
    - Stores raw API response as-is
    - Preserves original data (Bronze principle)
- Option 2: Spark DataFrame write
    - Adds schema inference
    - Introduces transformation
    

Used raw JSON ingestion to maintain data fidelity.

### Key Learnings
- Bronze layer should store raw, immutable data
- Avoid transforming data during ingestion
- Partitioning is critical for scalable data lakes
- Configuration should be reusable and modular
- Importing modules is better than chaining notebooks for shared logic

### Improvements Identified
- Add timestamp-based file naming for multiple runs per day
- Implement retry logic for API failures
- Add logging and monitoring
- Introduce incremental ingestion strategy

### Outcome
- Successfully built ingestion pipeline
- Stored raw API data in ADLS Bronze layer
- Implemented partitioning strategy
- Modularized configuration using reusable Python module

