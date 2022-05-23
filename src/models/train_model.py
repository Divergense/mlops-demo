import os
import click
import pickle
import mlflow
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv

from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error
from sklearn.ensemble import RandomForestRegressor

from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params


PARAMS = load_json_params(PARAMS_FILE)
MODEL_NAME=PARAMS['MODEL_NAME']
ARTIFACT_PATH = PARAMS['ARTIFACT_PATH']


load_dotenv()
mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
mlflow.set_experiment(MODEL_NAME)
mlflow.set_tag(key='ml stage', value='train')


@click.command()
@click.argument("data", type=click.Path(exists=True))
@click.argument("output_model", type=click.Path())
def train(data: str, output_model: str):
    RANDOM_STATE = PARAMS['RANDOM_STATE']
    Y_COLUMN = PARAMS['Y_COLUMN']
    MODEL_EXTENSION = PARAMS['MODEL_EXTENSION']

    output_model = Path(output_model)
    model_name = output_model.suffix
    if not model_name:
        output_model = output_model.parent
        output_model.joinpath(model_name + MODEL_EXTENSION)

    df = pd.read_csv(data)
    y = df[Y_COLUMN]
    x = df.drop(Y_COLUMN, axis=1)

    model = RandomForestRegressor(random_state=RANDOM_STATE)
    model.fit(x, y)
    y_pred = model.predict(x)

    with mlflow.start_run():
        mlflow.log_params(model.get_params())
        mlflow.log_params(PARAMS)
        # artifact_path is path deep inside S3 bucket store
        mlflow.sklearn.log_model(sk_model=model,
                                 artifact_path=ARTIFACT_PATH,
                                 registered_model_name=MODEL_NAME
                                 )
        mlflow.log_metrics(
            dict(
                mean_absolute_error=mean_absolute_error(y, y_pred),
                median_absolute_error=median_absolute_error(y, y_pred),
                r2_score=r2_score(y, y_pred)
            )
        )

    # output_model += MODEL_EXTENSION
    with open(output_model, "wb") as file:
        pickle.dump(model, file)
        print(f"Model {output_model} has been saved")


if __name__ == "__main__":
    train()
