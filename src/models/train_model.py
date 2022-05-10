import click
import pickle
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor


RANDOM_STATE = 12345
Y_COLUMN = "Rating"
MODEL_EXTENSION = ".pkl"


@click.command()
@click.argument("data", type=click.Path(exists=True))
@click.argument("output_model", type=click.Path())
def train(data: str, output_model: str):
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
