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
 