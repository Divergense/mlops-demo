import os
import json
import click
import pickle
import mlflow
import pandas as pd
import seaborn as sns

from pathlib import Path
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error

from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params


PARAMS = load_json_params(PARAMS_FILE)
MODEL_NAME = PARAMS["MODEL_NAME"]

"""
load_dotenv()
mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
"""

os.environ["MLFLOW_TRACKING_USERNAME"] = "rkchelebiev"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "d170e2430196df8c6d45714d14be8153a02e81d1"
mlflow.set_tracking_uri("https://dagshub.com/rkchelebiev/mlops-dvc-mlflow.mlflow")


@click.command()
@click.argument("input_model", type=click.Path(exists=True))
@click.argument("input_data", type=click.Path(exists=True))
@click.argument("output_metrics", type=click.Path())
def predict(input_model: str, input_data: str, output_metrics: str):
    Y_COLUMN = PARAMS["Y_COLUMN"]
    REPORT_PATH = Path(PARAMS["REPORT_PATH"])

    input_model = Path(input_model)
    with open(input_model, "rb") as file:
        model = pickle.load(file)
        model_name = input_model.name

    df = pd.read_csv(input_data)
    y_true = df[Y_COLUMN]
    x = df.drop(labels=[Y_COLUMN], axis=1)

    with mlflow.start_run():
        y_pred = model.predict(x)
        scores = dict(
            mean_absolute_error=mean_absolute_error(y_true, y_pred),
            median_absolute_error=median_absolute_error(y_true, y_pred),
            r2_score=r2_score(y_true, y_pred),
        )

        mlflow.set_experiment(MODEL_NAME)
        mlflow.set_tag(key="ml stage", value="evaluate")

        mlflow.log_params(model.get_params())
        mlflow.log_params(PARAMS)
        mlflow.log_metrics(scores)

    with open(output_metrics, "w") as file:
        json.dump(scores, file, indent=4)

    plt.figure(figsize=(12, 7))
    sns.histplot(y_true - y_pred, color="teal", label=model_name)
    plt.legend()
    plt.title("Model errors")
    plt.xlabel("Difference between trues and predictions")
    plt.savefig(REPORT_PATH.joinpath(model_name + ".png"))


if __name__ == "__main__":
    predict()
