## Day 1 – Setup, Storage Integration & Secure Access
# What I Set Up (Foundation)

- I started by setting up the basic infrastructure needed for the project.
- Used an existing Resource Group: rg-financial-datalake
- Created/used a Storage Account: financialdatalakestorage (with ADLS Gen2 enabled)
- Inside it, created a container: financial-data-project

# To follow the lakehouse pattern, I organized data into folders:

- bronze/ → raw data
- silver/ → cleaned data
- gold/ → business-ready data

# Then I set up Databricks:

- Created a workspace (trial tier)
- Created a cluster:
- Name: financial-us-cluster
- Type: Standard_D4s_v3
- Mode: USER_ISOLATION

Important: USER_ISOLATION means this cluster is aligned with Unity Catalog security model

# How I Connected Databricks to Storage
What I Tried First (and why it failed)

- I initially tried  dbutils.fs.mount()
- This is a common older approach to connect storage.  But it failed.
- Why it failed - Because my cluster is running in USER_ISOLATION mode, which:
    Blocks mounting
    Enforces stricter security rules
    Translation: mounts are considered legacy + less secure
- What Actually Worked
    Instead of mounting, I used direct access via ABFSS path. This is the modern approach.
    Example path: abfss://financial-data-project@financialdatalakestorage.dfs.core.windows.net/
    This allows direct read/write without mounting.

# Security Problem I Identified

- At first, I used a storage account key.But then I realized:
    It’s unsafe to hardcode secrets
    If pushed to GitHub → credentials leak
    Not acceptable in real projects
- I implemented a secure access pattern using Service Principal + Key Vault

# End-to-End Flow (Simple Explanation)
- Step 1 — Create identity -  Created a Service Principal in Microsoft Azure (like a machine user)
- Step 2 — Give permissions - 
        Assigned role: Storage Blob Data Contributor
        This allows access to ADLS
- Step 3 — Store secret safely -  
        Created Azure Key Vault
        Stored the client secret inside it
- Step 4 — Allow access to Key Vault
        Gave permission: Key Vault Secrets Officer
- Step 5 — Connect Key Vault to Databricks
        Created a Secret Scope (Key Vault-backed)
- Step 6 — Use secret inside notebook
        dbutils.secrets.get()
- Step 7 — Configure secure access
        Used OAuth config in Spark with:
        Client ID
        Tenant ID
        Secret (from Key Vault)
- Step 8 — Access data securely - Used the same ABFSS path: abfss://financial-data-project@financialdatalakestorage.dfs.core.windows.net/


# Key Takeaways: 
Mounts =  outdated in Unity Catalog setups
ABFSS direct access =  modern approach
Never hardcode secrets
Use: Service Principal + Key Vault + Secret Scopes
