import click
from typing import Tuple

from src.params_file import PARAMS_FILE
from src.utility.wrappers import read_process_write
from src.utility.processing import load_json_params


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--columns", multiple=True)
def drop_columns(input: str, output: str, columns: Tuple[str]):
    if len(columns) == 0:
        print(PARAMS_FILE)
        params = load_json_params(PARAMS_FILE)
        columns_list = params["UNNECESSARY_COLUMNS"]
    else:
        columns_list = list(columns)

    def process(df):
        df.drop(labels=columns_list, axis=1, inplace=True)
        print(f"Following columns: {columns_list} have been deleted")
        return [df]

    read_process_write(process, input=input, output=(output,))


if __name__ == "__main__":
    drop_columns()
