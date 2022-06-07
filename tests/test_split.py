import pandas as pd

from src import split
from click.testing import CliRunner


runner = CliRunner()


def test_cli_command():
    result = runner.invoke(split, 'data/interim/cleaned.csv data/interim/interim_train.csv data/interim/interim_test.csv')
    assert result.exit_code == 0


def test_output_size():
    df_train = pd.read_csv('data/interim/interim_train.csv')
    df_test = pd.read_csv('data/interim/interim_test.csv')
    assert df_train.shape[0] > 0 and df_test.shape[0] > 0
