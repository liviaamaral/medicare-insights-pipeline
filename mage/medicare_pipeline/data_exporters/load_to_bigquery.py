from google.cloud import bigquery
from google.oauth2 import service_account
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_bigquery(data, **kwargs) -> None:
    if isinstance(data, list):
        df = data[0]
    else:
        df = data

    credentials = service_account.Credentials.from_service_account_file(
        '/home/src/medicare_pipeline/credentials/medicare-de-project.json'
    )

    client = bigquery.Client(
        credentials=credentials,
        project='medicare-de-project'
    )

    table_id = 'medicare-de-project.medicare_insights.inpatient_2015'

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=[
            bigquery.SchemaField('drg_definition', 'STRING'),
            bigquery.SchemaField('provider_id', 'STRING'),
            bigquery.SchemaField('provider_name', 'STRING'),
            bigquery.SchemaField('provider_city', 'STRING'),
            bigquery.SchemaField('provider_state', 'STRING'),
            bigquery.SchemaField('total_discharges', 'INTEGER'),
            bigquery.SchemaField('average_covered_charges', 'FLOAT'),
            bigquery.SchemaField('average_total_payments', 'FLOAT'),
            bigquery.SchemaField('average_medicare_payments', 'FLOAT'),
            bigquery.SchemaField('out_of_pocket', 'FLOAT'),
        ],
        clustering_fields=['provider_state'],
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f'Loaded {len(df)} rows to {table_id}')