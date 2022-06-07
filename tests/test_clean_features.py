import pandas as pd
import great_expectations as ge

from src import clean_features
from click.testing import CliRunner


runner = CliRunner()


def test_cli_command():
    result_train = runner.invoke(clean_features, 'data/interim/interim_train.csv data/processed/processed_train.csv')
    result_test = runner.invoke(clean_features, 'data/interim/interim_test.csv data/processed/processed_test.csv')
    assert result_train.exit_code == 0 and result_test.exit_code == 0


def test_output():
    df_train = pd.read_csv('data/processed/processed_train.csv')
    df_test = pd.read_csv('data/processed/processed_test.csv')
    df_ge_train = ge.from_pandas(df_train)
    df_ge_test = ge.from_pandas(df_test)

    for col in df_train.columns:
        assert df_ge_train.expect_column_values_to_not_be_null(column=col).success is True
        assert df_ge_test.expect_column_values_to_not_be_null(column=col).success is True
