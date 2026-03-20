from mage_ai.settings.repo import get_repo_path
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from google.oauth2 import service_account
from google.cloud import storage
from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
import io

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        '/home/src/medicare_pipeline/credentials/medicare-de-project.json'
    )

    bucket_name = 'medicare-de-project-raw'
    object_key = 'inpatient/2015/medicare_inpatient_2015.parquet'

    client = storage.Client(credentials=credentials, project='medicare-de-project')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)

    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    blob.upload_from_file(buffer, content_type='application/octet-stream')

    print(f'Exported {len(df)} rows to gs://{bucket_name}/{object_key}')