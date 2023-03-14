#Readme

Dataset link: https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset

To download dataset through kaggle API. 

1. Setup Access to dataset

### Kaggle API

Official API for https://www.kaggle.com, accessible using a command line tool implemented in Python 3.  

Beta release - Kaggle reserves the right to modify the API functionality currently offered.

IMPORTANT: Competitions submissions using an API version prior to 1.5.0 may not work.  If you are encountering difficulties with submitting to competitions, please check your version with `kaggle --version`.  If it is below 1.5.0, please update with `pip install kaggle --upgrade`.

### Installation

Ensure you have Python 3 and the package manager `pip` installed.

Run the following command to access the Kaggle API using the command line:

`pip install kaggle` (You may need to do `pip install --user kaggle` on Mac/Linux.  This is recommended if problems come up during the installation process.) Installations done through the root user (i.e. `sudo pip install kaggle`) will not work correctly unless you understand what you're doing.  Even then, they still might not work.  User installs are strongly recommended in the case of permissions errors.

You can now use the `kaggle` command as shown in the examples below.

If you run into a `kaggle: command not found` error, ensure that your python binaries are on your path.  You can see where `kaggle` is installed by doing `pip uninstall kaggle` and seeing where the binary is.  For a local user install on Linux, the default location is `~/.local/bin`.  On Windows, the default location is `$PYTHON_HOME/Scripts`.

IMPORTANT: We do not offer Python 2 support.  Please ensure that you are using Python 3 before reporting any issues.

### API credentials

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`) and select 'Create API Token'. This will trigger the download of `kaggle.json`, a file containing your API credentials. Place this file in the location `~/.kaggle/kaggle.json` (on Windows in the location `C:\Users\<Windows-username>\.kaggle\kaggle.json` - you can check the exact location, sans drive, with `echo %HOMEPATH%`). You can define a shell environment variable `KAGGLE_CONFIG_DIR` to change this location to `$KAGGLE_CONFIG_DIR/kaggle.json` (on Windows it will be `%KAGGLE_CONFIG_DIR%\kaggle.json`).

For your security, ensure that other users of your computer do not have read access to your credentials. On Unix-based systems you can do this with the following command: 

`chmod 600 ~/.kaggle/kaggle.json`

You can also choose to export your Kaggle username and token to the environment:

```bash
export KAGGLE_USERNAME=datadinosaur
export KAGGLE_KEY=xxxxxxxxxxxxxx
```
In addition, you can export any other configuration value that normally would be in
the `$HOME/.kaggle/kaggle.json` in the format 'KAGGLE_<VARIABLE>' (note uppercase).  
For example, if the file had the variable "proxy" you would export `KAGGLE_PROXY`
and it would be discovered by the client.

To download the dataset with command line run: 

```
kaggle datasets download -d rsrishav/youtube-trending-video-dataset
```

2. Setup Cloud

2.1 Create a new google cloud project (dtc-de-youtube)

Navigate to dezoomcamp-project-youtube/1_setup_cloud/. 

``` 
terraform init
terraform plan
terraform apply
```
Enter your google cloud project id
https://www.youtube.com/watch?v=dNkEgO-CExg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12 (15:41)

2.2 Connect to VM from your PC

Create a /.ssh/config file and place below lines into it. 

```
Host de-zoomcamp-youtube
	Hostname 34.65.132.228
	User iamuser
	RemoteForward 52698 localhost:52698
	IdentityFile /home/antonis/.ssh/gcp
    LocalForward 8080 localhost:8080
    LocalForward 5432 localhost:5432
    LocalForward 8888 localhost:8888
    LocalForward 4200 localhost:4200
    LocalForward 4040 localhost:4040
```

Create SSH connection from your pc to the newly created VM
(create a passphrase if you want)

```
ssh-keygen -t rsa -f gcp_youtube -C iamuser -b 2048
cat gcp_youtube.pub
```

Copy and paste the output to 
https://console.cloud.google.com/compute/metadata?project=dtc-de-youtube&supportedpurview=project&tab=sshkeys. 

You can nw connect to the google cloud VM from your terminal with
```
ssh de-zoomcamp-youtube
```
2.3 Install anaconda with necessary configuration
```
sudo apt install wget
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
```

Initialize python
```
cd anaconda3
cd bin
./conda init bash
source ~/.bashrc
which python
```

2.4 Clone project to VM
```
git clone https://github.com/angeanto/dezoomcamp-project-youtube.git
```

2.5 Install docker

```
sudo apt-get update
sudo apt-get install docker.io
sudo gpasswd -a $USER docker
```
Log out and login again to refresh group permissions and run docker without sudo.

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
Run
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

2.6 Install pgcli
```
pip install pgcli
pgcli -h localhost -U root -d youtube
```
You should have succesfully logged in the pgcli 

2.7 Install psycopg2

```
cd -
conda install psycopg2
```

2.8 Connect pgadmin with postgres (not necessary)
https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=7 (5:10)


2.9 Move kaggle.json from local to remote in order the VM to has access to kaggle. 
```
put .kaggle/kaggle.json .kaggle
```

3. Download data
cd data
kaggle datasets download -d rsrishav/youtube-trending-video-dataset --force
sudo apt-get install unzip

SOS 30 GB disk for the gcs instance

4. Workflow orchestration

4.1 Create prefect workspace

install prefect and run prefect/orion server locally
```
pip install -U prefect
```
Run 1 time
```
!pip install prefect==2.7.7
!pip install prefect-sqlalchemy==0.2.2
!pip install prefect-gcp[cloud_storage]==0.2.4
!pip install protobuf==4.21.11
!pip installpandas-gbq==0.18.1
!pip install pyarrow==10.0.1
!pip install pandas-gbq==0.18.1
```
Run from ~/dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs
```
prefect orion start
prefect config set PREFECT_API_URL=http://localhost:4200/api
prefect block register -m prefect_gcp
```

4.2 Create prefect block for GCS 

https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20 (25:54)

Create locally the blocks.

GCP Credentials / zoom-gcp-creds
GCS / zoom-gcs

4.3 Create deployments

Run from directory: dezoomcamp-project-youtube/2_upload_data_to_postgres
```
prefect deployment build ./upload-data.py:etl_web_to_postgres -n "Web to Postgres"
```

4.3 Create deployments
Run from directory: dezoomcamp-project-youtube/2_upload_data_to_postgres
```
prefect deployment build ./upload-data.py:etl_web_to_postgres -n "Web to Postgres"
prefect deployment apply etl_web_to_postgres-deployment.yaml
```

Run from directory: dezoomcamp-project-youtube/3_upload_data_from_postgres_to_gcs
```
prefect deployment build ./move-data-to-gcs.py:etl_postgres_to_gcs -n "Postgres to GCS"
prefect deployment apply etl_postgres_to_gcs-deployment.yaml
```

Run from directory: dezoomcamp-project-youtube/4_upload_data_from_gcs_to_bq
```
prefect deployment build ./etl_gcs_to_bq.py:etl_gcs_to_bq -n "GCS to BQ"
prefect deployment apply etl_gcs_to_bq-deployment.yaml
```

You should be able to see the two deployments here http://localhost:4200/deployments

5. Create BQ table
on big query run 

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