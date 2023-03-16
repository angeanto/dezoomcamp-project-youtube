import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from time import time
import csv, math
from datetime import date
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.filesystems import GCS

@task(retries=3)
def fetch():
    """Read data from PostgreSQL database table and load into a DataFrame instance"""
    engine = create_engine('postgresql://root:root@localhost:5432/youtube')
    conn = engine.connect();
    df = pd.read_sql("SELECT * FROM youtube_data", conn);
    return df

@task()
def write_local(df: pd.DataFrame) -> Path:
    """Write DataFrame out locally as parquet file"""
    today = date.today()
    today = str(today).replace("-", "")
    today
    path = Path(f"/home/testuser/dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs/{today}.parquet")
    df.to_parquet(path, compression="gzip")
    return path, today

@task()
def write_gcs(path: Path, today) -> None:
    """Upload local parquet file to GCS"""
    path_gcs = 'youtube_data' 
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=f"{path_gcs}/{today}.parquet")
    return

@flow()
def etl_postgres_to_gcs() -> None:
    """The main ETL function"""
    
    df = fetch()
    path,today = write_local(df)
    write_gcs(path,today)

if __name__ == "__main__":
    etl_postgres_to_gcs()