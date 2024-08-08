from ingestion.bigquery import get_bigquery_client, get_bigquery_result, build_pypi_query
import os


def main ():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/alan_/.config/gcloud/service_account.json'
    df = get_bigquery_result(build_pypi_query(), get_bigquery_client('duckdb'))
    print('hello world')

if __name__ == '__main__':
    main()