hw_cookiecutter
==============================

google store app rating prediction

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
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
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Deploy MLflow tracking server of scenario number 4 in Docker

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

#### Minio

To run standalone MinIO on Docker:

```
$ docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  quay.io/minio/minio server /data --console-address ":9001"
```

If call above command without setting root user and password then default user and password will be 
`minioadmin:minioadmin` correspondingly.

*Note: variables `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` are equivalent to `MINIO_ACCESS_KEY` 
and `MINIO_SECRET_KEY` correspondingly.*

*Note: official documentation uses the following image of minio `quay.io/minio/minio` but starting 
docker-compose results in  download two images related to the service:`quay.io/minio/minio` and 
`minio/minio`. Probably sufficient condition of start the service is to use `minio/minio` image.*

#### Nginx

MinIO official documentation uses nginx server as proxy one. These configuration files are placed on: 
https://docs.min.io/docs/deploy-minio-on-docker-compose.

Create `nginx.conf` file in `./Docker` directory and fill it with required settings (example can be found 
on link mentioned previously).

*Question: what `:ro` does mean in nginx volume forward `./Docker/nginx.conf:/etc/nginx/nginx.conf:ro`?*

#### PostgreSQL and PGadmin
