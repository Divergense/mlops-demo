import click
from typing import Tuple
from src.utility.wrappers import read_process_write


UNNECESSARY_COLUMNS = ["Last Updated", "Current Ver", "Android Ver", "App"]


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--columns", multiple=True)
def drop_columns(input: str, output: str, columns: Tuple[str] = None):
    if len(columns) == 0:
        columns = UNNECESSARY_COLUMNS
    else:
        columns = list(columns)

    def process(df):
        df.drop(labels=columns, axis=1, inplace=True)
        print(f"Following columns: {columns} have been deleted")
        return [df]

    read_process_write(process, input=input, output=[output])


if __name__ == "__main__":
    drop_columns()
