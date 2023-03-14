import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from time import time
from pathlib import Path
import os
from sqlalchemy import text
import psycopg2
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.filesystems import GCS

engine = create_engine('postgresql://root:root@localhost:5432/youtube')
con = psycopg2.connect(database="youtube", user="root", password="root", host="localhost")

@task()
def download_data():
    os.system("kaggle datasets download -d rsrishav/youtube-trending-video-dataset --force")
    os.system("unzip -o youtube-trending-video-dataset.zip -d youtube-trending-video-dataset")
    os.system("rm youtube-trending-video-dataset.zip")
    
@task()
def drop_table():
    sql = text('DROP TABLE IF EXISTS youtube_data;')
    results = engine.execute(sql)

@task()
def upload_to_postgres():
    csv_directory = r'/home/testuser/dezoomcamp-project-youtube/2_upload_data_to_postgres/youtube-trending-video-dataset'
    for idx,filename in enumerate(Path(csv_directory).glob('*youtube_trending_data.csv')):
        t_start_files = time()
        df_iter = pd.read_csv(filename, iterator=True, chunksize=50000, sep = ',')
        print('Inserting file', filename)
        while True: 
            t_start = time()
            df = next(df_iter)
            df.to_sql(name='youtube_data', con=engine, if_exists='append')
            t_end = time()
            print('inserted another chunk, took %.3f second' % (t_end - t_start),filename)
            break
        t_end_files = time()
        print('inserted all csv files, took %.3f second' % (t_end_files - t_start_files))
    
@flow()
def etl_web_to_postgres() -> None:
    """The main ETL function"""
    download_data()
    drop_table()
    upload_to_postgres()

if __name__ == "__main__":
    etl_web_to_postgres()