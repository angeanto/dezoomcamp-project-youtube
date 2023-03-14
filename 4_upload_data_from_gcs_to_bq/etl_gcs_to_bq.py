from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from datetime import date

@task()
def extract_from_gcs():
    """Download youtube data from GCS"""
    today = date.today()
    today = str(today).replace("-", "")
    local =f"/home/iamuser/dezoomcamp-project-youtube/4_upload_data_from_gcs_to_bq/{today}.parquet"
    gcs_path = 'youtube_data'
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=local)
    return Path(f"{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print (len(df))
    return df

@task()
def write_bq(df: pd.DataFrame):
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    df.to_gbq(
    destination_table= "youtube_data_all.youtube_trends",
    project_id="dtc-de-youtube",
    credentials=gcp_credentials_block.get_credentials_from_service_account(),
    chunksize=500_000,
    if_exists="append",
    )
    
@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs()
    df = transform(path)
    write_bq(df)
    
if __name__ == "__main__":
    etl_gcs_to_bq()