import pandas as pd
import great_expectations as ge
from click.testing import CliRunner

from src import drop_columns
from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params


runner = CliRunner()
columns = ['Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price', 'Content Rating', 'Genres']


def test_cli_command():
    result = runner.invoke(drop_columns, 'data/raw/googleplaystore.csv data/interim/cleaned.csv')
    assert result.exit_code == 0


def test_output():
    df = pd.read_csv('data/interim/cleaned.csv')
    df_ge = ge.from_pandas(df)
    assert df_ge.expect_table_columns_to_match_ordered_list(column_list=columns).success is True
