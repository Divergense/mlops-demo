import click
import pickle
import pandas as pd

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params


@click.command()
@click.argument("data", type=click.Path(exists=True))
@click.argument("output_model", type=click.Path())
def train(data: str, output_model: str):
    params = load_json_params(PARAMS_FILE)
    RANDOM_STATE = params['RANDOM_STATE']
    Y_COLUMN = params['Y_COLUMN']
    MODEL_EXTENSION = params['MODEL_EXTENSION']

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

    # output_model += MODEL_EXTENSION
    with open(output_model, "wb") as file:
        pickle.dump(model, file)
        print(f"Model {output_model} has been saved")


if __name__ == "__main__":
    train()
