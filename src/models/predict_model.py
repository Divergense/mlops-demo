import click
import pickle
import pandas as pd
import seaborn as sns
from pathlib import Path
from matplotlib import pyplot as plt


Y_COLUMN = "Rating"
REPORT_PATH = Path("reports/figures/")


@click.command()
@click.argument("input_model", type=click.Path(exists=True))
@click.argument("input_data", type=click.Path(exists=True))
# @click.argument('y_true', type=click.Path(exists=True), default='')
def predict(input_model: str, input_data: str):
    input_model = Path(input_model)
    with open(input_model, "rb") as file:
        model = pickle.load(file)
        model_name = input_model.name

    df = pd.read_csv(input_data)
    y_true = df[Y_COLUMN]
    x = df.drop(labels=[Y_COLUMN], axis=1)

    y_pred = model.predict(x)

    plt.figure(figsize=(12, 7))
    sns.histplot(y_true - y_pred, color="teal", label=model_name)
    plt.legend()
    plt.title("Model errors")
    plt.xlabel("Difference between trues and predictions")
    plt.savefig(REPORT_PATH.joinpath(model_name + ".png"))


if __name__ == "__main__":
    predict()
