# Introduction
Welcome to this final project of Data Engineering Zoomcamp. Run the code below to reproduce the project on your own. Let me know if anything does not work properly. 

## Problem description
We have a postgres db which includes youtube trends data, running in a cloud VM. In the project, this data reach our postgres with [this](https://github.com/angeanto/dezoomcamp-project-youtube/blob/master/2_upload_data_to_postgres/upload-data.py) python script. Imagine that there's an application running behind the scenes which generates new records every day. In the project we perform the below operations (steps): 

- Upload the data from **kaggle** to the postgres which is running in our VM in Google Cloud.
- Move the data from the postgres to Google Cloud Storage.
- Move data from Google Cloud Storage to Big Query.
- Use dbt to create staging area materialized view and finally a fact table named fact_youtube_trends.
- Use Google Data Studio to visualize this table's data and create 2 tiles. 

**The final goal of this project is to move the data daily in a batch logic from the postgres db to Big Query using GCS (a Data Lake). Finally we use dbt for our analytics engineering and data consistency and visualize the fact the table with Google Data Studio. The project performs all these steps in a small scale but covers a 100% real scenario.**

## Cloud
The project is developed in the Google cloud and IaC tools Terraform and docker are used.
Important: Make sure to use **dtc-de-youtube** name for your google cloud project. 

## Data ingestion (batch) & Workflow orchestration
We do not use both spark and kafka. We use batch logic with prefect python and pandas code to move data between postgres --> gcs --> big query with prefect and relevant dags.

THe project uses 3 prefect deployments: 
- etl-web-to-postgres: Uploads data from kaggle to postgres (Scheduled to run daily 18:05)
- etl-postgres-to-gcs: Moves data from postgres to GCS (Scheduled to run daily 18:15)
- etl-gcs-to-bq: Moves data from GCS to Big Query (Scheduled to run daily 18:25)

All the scripts make use of today's date function. Make sure when testing, to run these 3 deployments the same day in order to move the file names properly. The code is parameterized to schedule them with a 10 minute difference. 

## Data warehouse
Big Query is used. Make sure to use dtc-de-youtube name for your google cloud project.
dbt creates a clusterer and partioned table in a way that makes sense. 
The file [models/core/fact_youtube_trends.sql](https://github.com/angeanto/dezoomcamp-project-youtube/blob/master/models/core/fact_youtube_trends.sql) creates a fact table cluster by `categoryId`. That way our queries commonly filter on this particular column. Clustering accelerates queries because the query only scans the blocks that match the filter. Our queries filter on columns that have many distinct values (high cardinality). Clustering accelerates these queries by providing BigQuery with detailed metadata for where to get input data. Furthermore, the fact table is partitioned by date field `trending_date_timestamp`. Table partitioning is a technique for splitting large tables into smaller ones. When you partition a table and then execute a query, it is also BigQuery that determines which partition to access and minimizes the data that must be read. A partitioned table is a table divided to sections by partitions. Dividing a large table into smaller partitions allows for improved performance and reduced costs by controlling the amount of data retrieved from a query.Clustering sorts the data based on one or more columns in the table. The order of the clustered columns determines the sort order of the data. Clustering can improve the performance of certain types of queries, such as queries that use filter clauses and queries that aggregate data.

## Transformations (dbt, spark, etc)
We use dbt to create staging materialized views (the idea is to process anything there) and finally a fact table named fact_youtube_trends.

## Dashboard
- Used Google Data Studio to visualize this table's data and create 2 tiles. Visit https://lookerstudio.google.com/reporting/48a8f184-3605-4071-bf52-4edcb49882bf
and check the 2 created tiles. 

## Reproducibility
Hope below guide helps reproduce anything succesfully. 

# How to reproduce the project

## Setup Cloud & IaC tools (Terraform,Docker)

**Create a new google cloud project named dtc-de-youtube (keep the name same, otherwise it won't work)**

Now, navigate to dezoomcamp-project-youtube/1_setup_cloud/terraform 

``` 
terraform init
terraform plan
terraform apply
```
Enter your google cloud project id
https://www.youtube.com/watch?v=dNkEgO-CExg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12 (15:41)

### Connect to VM from your PC

In your local machine create a /.ssh/config file
```
mkdir .ssh
touch config
```
and place below lines into it. 
```
Host de-zoomcamp-youtube
	Hostname <ip_of_your_virtual_machine>
	User testuser
	RemoteForward 52698 localhost:52698
	IdentityFile /home/antonis/.ssh/gcp_test_user
    LocalForward 8080 localhost:8080
    LocalForward 5432 localhost:5432
    LocalForward 8888 localhost:8888
    LocalForward 4200 localhost:4200
    LocalForward 4040 localhost:4040
```

Create SSH connection from your pc to the newly created VM
(Let passphrase empty for simplicity)

```
cd .ssh
ssh-keygen -t rsa -f gcp_test_user -C testuser -b 2048
cat gcp_test_user.pub
```

Copy and paste the output to 
https://console.cloud.google.com/compute/metadata?project=dtc-de-youtube&supportedpurview=project&tab=sshkeys. 

You can now connect to the google cloud VM from your terminal with
```
ssh de-zoomcamp-youtube
```
YOU ARE NOW LOGGED IN THE VM MACHINE. Run everything there. 


### Clone the repo in the Virtual Machine

```
sudo apt update
sudo apt install git
git clone https://github.com/angeanto/dezoomcamp-project-youtube.git
```

### Install anaconda with necessary configuration

```
sudo apt-get install wget
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
```

Initialize python
```
cd anaconda3/bin
./conda init bash
source ~/.bashrc
which python
```

### Setup access to dataset

Dataset link: https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset

To download dataset through kaggle API. 

#### API credentials

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`) and select 'Create API Token'. This will trigger the download of `kaggle.json`, a file containing your API credentials. Place this file in the location `~/.kaggle/kaggle.json` (on Windows in the location `C:\Users\<Windows-username>\.kaggle\kaggle.json` - you can check the exact location, sans drive, with `echo %HOMEPATH%`). You can define a shell environment variable `KAGGLE_CONFIG_DIR` to change this location to `$KAGGLE_CONFIG_DIR/kaggle.json` (on Windows it will be `%KAGGLE_CONFIG_DIR%\kaggle.json`).

#### To download the dataset with command line run: 

Install kaggle on anaconda
```
conda install -c conda-forge kaggle
```

Setup kaggle.json file with credentials
on the starting directory of VM run

```
mkdir .kaggle
```
then from your local machine (where you have downloaded the kaggle.json file) move kaggle.json to vm. 

```
put .kaggle/kaggle.json .kaggle
```

Connect with sftp
```
sftp de-zoomcamp-youtube

```

and run (dont run it, script includes the command)
```
kaggle datasets download -d rsrishav/youtube-trending-video-dataset
```

### Install docker & unzip(to unzip downloaded files from kaggle)

```
sudo apt-get update
sudo apt-get install unzip
sudo apt-get install docker.io
sudo gpasswd -a $USER docker
```
Log out (Ctrl + D) and login again to refresh group permissions and run docker without sudo.

Add docker path to .bashrc

```
cd --
mkdir bin
cd bin/
wget https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64
chmod +x docker-compose-linux-x86_64
./docker-compose-linux-x86_64 version
cd
nano .bashrc
```
Add
```
export PATH="${HOME}/bin:${PATH}"
```
Press ctrl + O to save the file. 
Press ctrl + X to exit 

Now Run
```
source .bashrc
which docker-compose-linux-x86_64
```
You should see the relevant path
and by running from the root directory
```
docker-compose-linux-x86_64 version
```
you should see the relevant version

From the root directory of the project navigate to 
```
cd 1_setup_cloud
```
and run 
```
docker-compose-linux-x86_64 up -d
```

### Install libraries
```
pip install -r requirements.txt
conda install psycopg2
```

### Test that postgres is running
```
pip install pgcli
pgcli -h localhost -U root -d youtube
```
You should have succesfully logged in the pgcli 

1.8 Connect pgadmin with postgres (not necessary)
https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=7 (5:10)


## Workflow orchestration

### Create prefect workspace

install prefect and run prefect/orion server in the VM
```
pip install -U prefect
```

Run from ~/dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs
```
prefect orion start
```
open a new terminal navigate to /dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs and run
```
prefect config set PREFECT_API_URL=http://localhost:4200/api
```

### Create prefect block for GCS 

https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20 (25:54)

Create locally the blocks.

GCP Credentials / zoom-gcp-creds
GCS / zoom-gcs

Run 
```
prefect block register -m prefect_gcp
```

### Create deployments (we'll schedule them with 10 minutes difference)
Run from directory: dezoomcamp-project-youtube/2_upload_data_to_postgres
```
prefect deployment build ./upload-data.py:etl_web_to_postgres --cron "5 18 * * *" -n "Web to Postgres"
prefect deployment apply etl_web_to_postgres-deployment.yaml
```

Run from directory: dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs
```
prefect deployment build ./move-data-to-gcs.py:etl_postgres_to_gcs --cron "15 18 * * *" -n "Postgres to GCS"
prefect deployment apply etl_postgres_to_gcs-deployment.yaml
```

Create BQ table on big query run 

```
CREATE TABLE `youtube_data_all.youtube_trends`
(
index INTEGER,
video_id STRING,
title STRING,	
publishedAt	STRING,	
channelId STRING,	
channelTitle	STRING,	
categoryId INTEGER,	
trending_date STRING,	
tags STRING,	
view_count INTEGER,	
likes INTEGER,	
dislikes INTEGER,	
comment_count INTEGER,	
thumbnail_link STRING,	
comments_disabled BOOLEAN,	
ratings_disabled BOOLEAN,	
description STRING
);
```
Run from directory: dezoomcamp-project-youtube/4_upload_data_from_gcs_to_bq
```
prefect deployment build ./etl_gcs_to_bq.py:etl_gcs_to_bq --cron "25 18 * * *" -n "GCS to BQ"
prefect deployment apply etl_gcs_to_bq-deployment.yaml
```

You should be able to see the 3 deployments here http://localhost:4200/deployments

### Start an agent to create scheduled deployments

Open a new VM terminal and run (Important: YOU SHOULD ALWAYS HAVE TO RUN THIS COMMAND EVERY TIME YOU TURN ON AND OFF THE GOOGLE CLOUD VM)

```
prefect agent start --work-queue "default"
```

You can either modify the code to test the functionality of scheduling the deployments or run them instantly from the Orion server UI. 

Run:
1. Web to Postgres
2. Postgres to GCS
3. GCS to BQ

## DBT

Login to your dbt account or create a new one, because dbt free developer policy allows 1 single project.

Now connect dbt with BigQuery following one by one the [instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md).

DO NOT CREATE THE BIG QUERY DATASET FROM DBT ENVIRONMENT. Create it from BigQuery and select the same region with your project. I ran it setting everything in Europe-West-6. 

Name your dataset dbt_youtube (SOS). 

Add your forked github repository following the instructions above at 
**Add GitHub repository** section. Clone with ssh.

Click start development in the IDE.

run

```
dbt deps
dbt run
```
You can now check that materialized view and fact table exists. 

## Google Data Studio

Visit https://lookerstudio.google.com/reporting/48a8f184-3605-4071-bf52-4edcb49882bf
and check the 2 created tiles. 
