from ingestion.bigquery import (
    get_bigquery_client,
    get_bigquery_result,
    build_pypi_query,
)
import os
from ingestion.models import PypiJobParameters
import fire
import duckdb

def main(params: PypiJobParameters):
    df = get_bigquery_result(
        query_str=build_pypi_query(params),
        bigquery_client=get_bigquery_client(project_name=params.gcp_project),
    )
    print(df)
    conn = duckdb.connect()
    conn.sql("COPY (SELECT * FROM df) TO 'data/duckdb.csv'")
    print(os.getcwd())
    print("csv saved at data/duckdb.csv")


if __name__ == "__main__":
    fire.Fire(lambda **kwargs: main(PypiJobParameters(**kwargs)))
