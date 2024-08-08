from ingestion.bigquery import (
    get_bigquery_client,
    get_bigquery_result,
    build_pypi_query,
)
import os
from ingestion.models import PypiJobParameters
import fire


def main(params: PypiJobParameters):
    df = get_bigquery_result(
        build_pypi_query(), get_bigquery_client(params.gcp_project)
    )
    print(df)
    
    print("hello world")


if __name__ == "__main__":
    fire.Fire(lambda **kwargs: main(PypiJobParameters(**kwargs)))
