# Introduction

## Problem description

## Cloud

## Data ingestion (batch) & Workflow orchestration

## Data warehouse

## Transformations (dbt, spark, etc)

## Dashboard

## Reproducibility


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

Open a new VM terminal and run

```
prefect agent start --work-queue "default"
```

You can either modify the code to test the functionality of scheduling the deployments or run them instantly from the Orion server UI. 

Run:
1. Web to Postgres
2. Postgres to GCS
3. GCS to BQ

## DBT