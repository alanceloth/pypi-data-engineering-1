from google.cloud import bigquery
from google.oauth2 import service_account
from google.auth.exceptions import DefaultCredentialsError
import pandas as pd
import time
from loguru import logger
import os

def get_bigquery_client(project_name: str) -> bigquery.Client:
    """Get BigQuery Client"""

    try:
        service_account_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if service_account_path:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
            bigquery_client = bigquery.Client(
                project=project_name, credentials=credentials
            )
            return bigquery_client
        
        raise EnvironmentError(
            "No valid credentials found for BigQuery auth"
        )
    except DefaultCredentialsError as creds_error:
        raise creds_error
    

def get_bigquery_result(
        query_str: str, bigquery_client: bigquery.Client
) -> pd.DataFrame:
    """Get query result from BigQuery and yield rows as dictionaries."""

    try:
        start_time = time.time()
        logger.info(f"Running query: {query_str}")        
        dataframe = bigquery_client.query(query_str).to_dataframe()
        elapsed_time = time.time() - start_time
        logger.info(f"Query executed and data loaded in {elapsed_time:.2f} seconds")
        return dataframe
    
    except Exception as e:
        logger.error(f"Error running query: {e}")
        raise

def build_pypi_query() -> str:
    return f"""
    SELECT * 
    FROM 
        `bigquery-public-data.pypi.file_downloads` 
    WHERE 
        project = 'duckdb'
        AND timestamp >= TIMESTAMP("2024-08-06")
        AND timestamp < TIMESTAMP("2024-08-07")
"""

# gcloud projects add-iam-policy-binding pypi-data-engineering-1 \
#     --member=serviceAccount:dev-pypi@pypi-data-engineering-1.iam.gserviceaccount.com \
#     --role=roles/bigquery.jobUser
