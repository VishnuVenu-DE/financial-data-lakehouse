# Day 3 – Silver Layer Transformation & Production-Grade Setup

## Objective
Transform raw Bronze data into structured, queryable format (Silver layer) while aligning with production-grade practices such as version control and governed data access using Unity Catalog.

---

#  Part 1: Databricks + GitHub Integration

## Problem
- Initially developed notebooks in Databricks and manually downloaded them to local system for GitHub commits
- This approach was inefficient and not scalable

## Solution
- Integrated Databricks workspace with GitHub using Databricks Repos

## Steps
1. Generated Personal Access Token (PAT) in GitHub
2. Connected GitHub in Databricks (User Settings → Git Integration)
3. Cloned repository using Databricks Repos
4. Moved all notebooks and scripts into repo structure

## Updated Project Structure

financial-data-lakehouse/
├── common_scripts/
│   └── common_functions.py
├── notebooks/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/

## Key Learning
- Databricks Repos eliminates manual export/import workflow
- Enables direct commit and push from Databricks

---

# Part 2: Silver Layer Transformation

## Objective
Convert raw JSON data into structured format for analytics

## Steps Performed

### 1. Read Bronze Data
- Loaded raw JSON from ADLS Bronze path

### 2. Data Cleaning
- Selected required fields
- Applied data type casting
- Removed unnecessary columns

### 3. Deduplication
- Removed duplicate records based on key columns

### 4. Data Storage
- Stored cleaned data in Delta format in ADLS Silver layer, partitioned by load_date

## Key Learning
- Silver layer is responsible for schema enforcement and data quality
- Separation of raw and processed data is critical
- Delta format enables reliability and performance

---

# Part 3: External Table Setup (Unity Catalog)

## Initial Issue
- Attempted to create external table using:

CREATE TABLE ... LOCATION 'abfss://...'

- Error encountered:
NO_PARENT_EXTERNAL_LOCATION_FOR_PATH

## Root Cause
- Unity Catalog requires:
  - Storage Credential
  - External Location
  - Proper permissions

---

# 🧠 Approach Evolution

### Attempt 1
- Tried SQL-based creation of storage credential
- Failed due to permission restrictions
- Genie AI suggested to create Managed tables but I wanted to replicate production scenarios hence explored for creating External table

---

# Final Implementation (Production Pattern)

## Step 1: Created Access Connector
- Used Azure Databricks Access Connector (Managed Identity)
- Eliminated need for client secrets

## Step 2: Assigned RBAC Role
- Role: Storage Blob Data Contributor
- Assigned to Access Connector on ADLS

## Step 3: Created Storage Credential (UI)
- Created new credential & Used Access Connector as authentication method

## Step 4: Created External Location
- Mapped ADLS container path
- Linked with storage credential

## Step 5: Granted Permissions
- Provided READ FILES and WRITE FILES access

## Step 6: Created External Table

CREATE TABLE financial_project_db.silver_crypto
USING DELTA
LOCATION 'abfss://financial-data-project@financialdatalakestorage.dfs.core.windows.net/silver/crypto';

---

# Key Learnings

- Unity Catalog enforces strict governance over data access
- External tables require pre-configured credentials and locations
- Managed Identity (Access Connector) is preferred over secrets
- Separation of:
  - Compute (Databricks)
  - Storage (ADLS)
  - Governance (Unity Catalog)
  is essential in production

---

# Design Decisions

## External Table vs Managed Table

| Option | Decision |
|------|--------|
| Managed Table | Avoided |
| External Table | Implemented |

### Reason
- Provides full control over storage
- Aligns with enterprise data architecture
- Enables data sharing across systems

---

#  Issues Faced & Fixes

## Issue 1: CREATE STORAGE CREDENTIAL not working
- Cause: Lack of required privileges
- Fix: Used UI-based setup

## Issue 2: Missing "Auth Type" in UI
- Cause: Workspace configuration difference
- Fix: Used Access Connector approach

## Issue 3: RBAC Permission Errors
- Cause: Missing role assignment or propagation delay
- Fix:
  - Assigned correct role
  - Waited for propagation

## Issue 4: External Location Not Recognized
- Cause: Not registered in Unity Catalog
- Fix: Created external location properly

---

# 🚀 Final Outcome

- Successfully transformed Bronze data into structured Silver layer
- Stored data in Delta format in ADLS
- Created governed external table using Unity Catalog
- Established secure access using Managed Identity
- Integrated Databricks with GitHub for seamless development

---