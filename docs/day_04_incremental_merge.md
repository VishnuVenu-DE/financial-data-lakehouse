# Day 4 – Incremental Processing (MERGE) & Key Learnings

## Objective
Build an incremental data pipeline that:
- Avoids duplicate data
- Maintains latest state correctly
- Supports historical tracking
- Ensures idempotent behavior

---

## Architecture Evolution

### Initial Approach
- Bronze: Raw data (append-only)
- Silver: Overwrite or append

### Problems Identified
- Overwrite → data loss
- Append → duplicates on rerun

### Final Design

| Layer | Table | Strategy |
|------|------|----------|
| Bronze | Raw JSON | Append |
| Silver | silver_crypto_history | MERGE (insert-only behavior) |
| Silver | silver_crypto_latest | MERGE (update + insert) |

---

## Table Design Decisions

### History Table
- Stores all historical records
- Prevents duplicate entries for same coin and date
- Behaves like append but with deduplication

### Latest Table
- Stores only latest record per coin
- Updates existing rows when newer data arrives

---

## Key Issues Faced & Resolutions

### 1. MERGE Fails with Missing Column
- Root cause: Table created on empty location without schema
- Fix: Ensure schema exists before MERGE (pre-write data or define schema)

---

### 2. Confusion About Initial Load
- Assumption: MERGE needs initial insert
- Reality: MERGE handles both initial and incremental loads automatically, provided table is created beforehand. 
- Requirement: INSERT clause must be present

---

### 3. Duplicate Data on Reruns
- Cause: Using append mode blindly
- Incorrect fix: Delete + append
- Correct fix: Use MERGE for idempotent processing

---

### 4. Incorrect MERGE Condition
- Issue: Using multiple conditions with AND
- Impact: Valid updates skipped
- Fix: Use only ingestion timestamp for freshness logic

---

### 5. Naming Confusion
- Attempted: generic incremental table name
- Problem: unclear purpose
- Fix: use clear naming
  - history table for full data
  - latest table for snapshot

---

### 6. SCD Type 2 Misunderstanding
- Thought: needed for history tracking
- Reality: data is time-series, not dimensional
- Decision: avoid SCD2, use append + merge pattern

---

## Key Learnings

### 1. MERGE is Universal
- Handles both initial load and incremental updates
- No separate initialization logic required

---

### 2. Idempotency is Critical
- Pipeline should produce same result on repeated runs
- Achieved using proper MERGE conditions

---

### 3. Avoid Delete + Reload
- Leads to data loss risks
- Not production-safe
- Inefficient and hard to debug

---

### 4. Separate History and Latest Logic
- History → for analytics and trends
- Latest → for dashboards and real-time views

---

### 5. Use Timestamps Correctly
- ingestion_time → determines freshness
- ingestion_date → used for partitioning and filtering

---

### 6. Schema Awareness is Important
- External tables do not infer schema from empty paths
- Schema must exist before performing operations like MERGE

---

### 7. Simplicity Over Over-Engineering
- Adding more conditions can break logic
- Minimal and correct conditions are preferred

---

