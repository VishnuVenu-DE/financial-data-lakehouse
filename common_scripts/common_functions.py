def setup_adls_access():
    client_id = dbutils.secrets.get(scope="financial-scope", key="adls-client-id2")
    tenant_id = dbutils.secrets.get(scope="financial-scope", key="adls-tenant-id")
    client_secret = dbutils.secrets.get(scope="financial-scope", key="adls-client-secret")

    spark.conf.set(
        "fs.azure.account.auth.type.financialdatalakestorage.dfs.core.windows.net",
        "OAuth"
    )

    spark.conf.set(
        "fs.azure.account.oauth.provider.type.financialdatalakestorage.dfs.core.windows.net",
        "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
    )

    spark.conf.set(
        "fs.azure.account.oauth2.client.id.financialdatalakestorage.dfs.core.windows.net",
        client_id
    )

    spark.conf.set(
        "fs.azure.account.oauth2.client.secret.financialdatalakestorage.dfs.core.windows.net",
        client_secret
    )

    spark.conf.set(
        "fs.azure.account.oauth2.client.endpoint.financialdatalakestorage.dfs.core.windows.net",
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    )

    print("ADLS access setup complete.")


