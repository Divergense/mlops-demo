import click
from sklearn.model_selection import train_test_split

from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params
from src.utility.wrappers import read_process_write


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", nargs=2, type=click.Path())
@click.option("--test_size", "-t", type=click.FLOAT, default=0.8)
def split(input: str, output: str, test_size: float = 0.8):
    """
    Split input dataframe into 2 subsets.
    Args:
        input - path to source data file
        output -
    """
    params = load_json_params(PARAMS_FILE)
    RANDOM_STATE = params['RANDOM_STATE']

    def process(df):
        df_train, df_test = train_test_split(
            df, test_size=test_size, random_state=RANDOM_STATE
        )
        return df_train, df_test

    read_process_write(process, input=input, output=output)


if __name__ == "__main__":
    split()
