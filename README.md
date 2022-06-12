Google Store App rating prediction
==============================

TODO:

- gitlab-cd


## Machine learning core of the project

The goal of the ml project part is to predict google play store application rating.

The dataset was build from web scraped data of 10k Play Store apps for analysing the Android market.
The dataset consists of 2 files `googleplaystore.csv` and `googleplaystore_user_reviews.csv`.
This project uses only one file - `googleplaystore.csv` as general goal of the project is MLOps not ML.

For details see original page of the dataset: <https://www.kaggle.com/datasets/lava18/google-play-store-apps>.

Some columns are unnecessary and was dropped: `"Last Updated", "Current Ver", "Android Ver", "App"`.

Some columns have 'mixed' format also. For example `Installs` column describes number of installs with two 
formats: `number{K|M}` or plain integer `number`. All columns with format like this was converted to integers.

Data contains also missing values. App with missing `Rating` value was just dropped. Other column values was 
replaced: for example values of column `Size` (size of app in megabytes) replaced with median size of all apps.

Rating prediction is considered as regression task. For solving the task was chosen random forest regressor algorithm.
For algorithm evaluation are used the following metrics: r2 score, mean absolute error and median absolute error.

After training the ML model the project scripts generate and save histogram of residuals between predicted and actual 
ratings in png format.


## MLOps approaches

система контроля версий
### Source version control system

For control source code versions is used Git with self-hosted Gitlab on remote server under Docker.
On the same server was deployed Gitlab Runner in Docker also.

See following image for resulting usage of the system:

![](./reports/figures/git_history.png)

### Codestyle control tools

Black python package is used for automated code formatting.

In addition, mypy and flake8 python packages was integrated in gitlab CI.

Mypy is a python package for type checking, flake8 checks code for corresponding code formatting.

By default, black setting differs from flake8 one. To avoid conflicts (maximum length of the line) flake8 
was setting up to black settings in `tox.ini` file.

### Project template tool

For creating a logical, reasonably standardized, but flexible project structure was chosen 
Cookiecutter Data Science. The project based on the 
<a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter 
data science project template</a>.

All that it's need install cookiecutter via pip and call:

```
cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science
```

But during project progress was added some files, directories and deleted unnecessary files. 
Resulting project organization looks like this:

------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    ├── Docker             <- Code for docker-compose services
    │   ├── fastapi_model_service
    │   ├── mlflow_image
    │   └── nginx.conf
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests
    │   ├── __init__.py
    │   ├── test_clean_features.py
    │   ├── test_drop_columns.py
    │   └── test_split.py
    ├── dvc.lock
    ├── dvc.yaml
    ├── params.json
    ├── poetry.lock
    ├── pyproject.toml
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

--------


### Workflow

As workflow managers was tried Snakemake and DVC. Since DVC supports data versioning with workflow manager 
the final decision is to use exactly DVC.

To store data remotely DVC uses <https://dagshub.com/> service and Minio hosted as docker service. Also 
DVC was set up to track metrics. To get detail info see `dvc.yaml` file.

Resulting DVC pipeline is following:

![](./reports/figures/dvc_pipeline.png)

### Experiment tracking tools

Record and query experiments are performed via MLflow platform. The project uses MLflow tracking server 
hosted in `https://dagshub.com/` and in own docker-compose service.

### Testing tools

The standard of testing python code is pytest package that is used in the project too. To run unit tests 
was created tests package and integration test performed along with `dvc repro` procedure. All these 
tools was included in gitlab CI.

### Continuous integration pipeline

For CI is used `.gitlab-ci.yml` that has two stages: static analysis and unit tests with integration tests.

## Project deployment

Deploy MLflow tracking server of scenario number 4 in Docker

### 1. Storing environment variables  

These variables are stored in `.env` file but must be added to `.gitignore` for safety reasons and `.env.example` 
is tracking under VCS. `.env.example` file stores only key of variables not values!

### 2. Source docker files

Create directory for example `Docker` under project root.

```
$ mkdir Docker
```

### 3. Services

Core of the deployed app will correspond to MLflow tracking server of scenario 4:

![](./reports/figures/scenario_4.png)

Thus, the app will consist of the following services:

- S3 storage (minio) host;
- Nginx proxy server of S3 host for load balance;
- MLflow tracking server;
- PostgreSQL database;
- PgAdmin server for  postgresql db.

### 4. docker-compose.yaml

This file will start all defined images that handle all defined services.

Create `docker-compose.yaml` file and describe all services:

```
$ vim docker-compose.yaml
```

*Note: docker-compose can use environment variables. For this it is necessary to have `.env` 
file in the same directory of the `docker-compose.yaml`.*

To check `docker-compose.yaml` file run:

```
$ docker-compose config
```

### 5. Minio

Command example of running standalone MinIO on Docker:

```
$ docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  quay.io/minio/minio server /data --console-address ":9001"
```

If call above command without setting root user and root password then default user and password will be 
`minioadmin:minioadmin` correspondingly.

**Important:** After start minio service it is necessary to create s3 bucket with name equals to environment 
variable `MINIO_S3_BUCKET`.

*Note: variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` are equivalent to `MINIO_ACCESS_KEY` 
and `MINIO_SECRET_KEY` correspondingly. MinIO warning recommends to use first variant.*

*Note: official documentation uses the following image of minio `quay.io/minio/minio` but starting 
docker-compose results in  download two images related to the service:`quay.io/minio/minio` and 
`minio/minio`. Probably sufficient condition of start the service is to use `minio/minio` image.*

### 6. Nginx

MinIO official documentation uses nginx server as proxy one. These configuration files are placed on: 
https://docs.min.io/docs/deploy-minio-on-docker-compose.

Create `nginx.conf` file in `./Docker` directory and fill it with required settings (example can be found 
on link mentioned above).

*Question: what `:ro` does mean in nginx volume forward `./Docker/nginx.conf:/etc/nginx/nginx.conf:ro`?*

### 7. PostgreSQL and PGadmin

Configures can be seen in `docker-compose.yaml` it is pretty standard.

1. **Important:** before start mounted host volume MUST belong to 5050 user id and the same group id.
This id corresponds to pgadmin user/group somehow:

    ```
    $ mkdir ./Docker/pgadmin
    $ sudo chown -R 5050:5050 ./Docker/pgadmin
    ```

2. After starting the containers need to add new server at PGadmin that is accessible on `127.0.0.1:5050` as 
defined in `docker-compose.yaml`:

    - set to `Host name/addres` field ip address of the postgresql database. To find out required ip 
   first search for container id of postgresql service:
    
        ```
        $ docker ps
        ```
      
        Then use docker inspect command to list configuration of the container. Required ip address can be found 
        at section `Networks`:
    
        ```
        $ docker inspect 3c982a5b3e76
        ```
    - fields `Maintenance database`, `Username`, `Password` must equal to environment values of postgresql service:
    `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` correspondingly.


*Note: PGadmin can be proxied through Nginx as Minio also (see official documentation).*

### 8. MLflow tracking server

1. Create Dockerfile in `./Docker/mlflow_image/` that based on python 3.9 image and installs `mlflow`, `boto3` and 
   `psycopg2` python packages. 

2. Include in `docker-compose.yaml` command that build image from the Dockerfile.

*Note: MLflow obtains credentials to access S3 from `~/.aws/credentials` or environment variables 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` depending on which of these are available.*

### 9. Built-in deployment MLflow models

#### Local environment

To run MLflow server for model serving type:

```
$ mlflow models serve --no-conda -m path_to_model -h 0.0.0.0 -p 8001
```

Argument `path_model` can be obtained from MLflow UI in field `Full Path` under specific experiment.

**Important:** before run the server it is needed to set environment variables `AWS_ACCESS_KEY_ID`, 
`AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET_NAME` to proper values:

```
$ export AWS_ACCESS_KEY_ID=minioadmin
$ export AWS_SECRET_ACCESS_KEY=minioadmin
$ export AWS_S3_BUCKET_NAME=app-ratings
```

While the sever deployed it is possible send POST request on `http://127.0.0.1:8001/invocations` with 
JSON body that has `"columns"` and `"data"` properties and corresponding values in array format. 

#### Docker environment

```
$ mlflow models build-docker -m path_to_model -n image_name
$ docker run image_name -p p_out:p_in
```

### 10. External tools for deployment MLflow models

#### FastAPI

1. Create Dockefile in `Docker/fastapi_model_service`.

2. Create directory `app` in `./Docker/fastapi_model_service`. Place application code in this directory.

*Note: docker is not able to copy files from outside of Dockerfile directory.*

4. Include the application in `docker-compose.yaml`.

### 11. General concepts of deployment

Some important concepts are:

- Security - HTTPS
- Running on startup
- Restarts
- Replication (the number of processes running)
- Memory
- Previous steps before starting

For details read <https://fastapi.tiangolo.com/deployment/concepts/>


## Project issues and possible solutions

### Initialization issues

#### Init raw files

After cloning repo raw files don't exist:

- Configure gdrive remote storage:

  1. Create folder in gdrive and cd into it.
  2. Copy last part of uri.
  3. Add remote storage:
      ```
     $ dvc remote add -d gdrive://copied-last-part-uri
      ```
  4. Push data to remote storage:
      ```
     $ dvc push
      ```
  5. Follow dvc instructions: go to proposed url and give access rights to dvc.

- use <https://dagshub.com> service.

#### Init minio

1. To create necessary bucket automatically use minio API available on python, js, java, go. 
All these have method that can create buckets.

2. Is there necessary to include raw files in minio while first initialization?

#### Init pgadmin

To create pgadmin connection use some configurations file:

1. For pre configuration see <https://stackoverflow.com/questions/64620446/adding-postgress-connections-to-pgadmin-in-docker-file>.

2. Before start the service it is need bash script that sets required permissions to `pgadmin` volume.

#### Init fastapi service

- add checking model exists when fastapi_model_service starts

- before run services need to dvc repro since it creates models for fastapi_model_service

- 'fastapi_model_service' uses '.env', 'pyproject.toml' and 'poetry.lock' files - that is no DRY


#### Required permissions to `pgadmin` directory

It's need some simple script like described above that is executed before docker-compose start services.

### Deployment issues

- need https support

- load balancers for all services

- arguments of python package are not in configuration file that results in dvc and test duplicate code

- testing the service requires deployment all services before it

## Team

There is one member of the project - the author Raphych.
