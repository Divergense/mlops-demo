import json
import pandas as pd


def load_json_params(file_path):
    with open(file_path, 'r') as file:
        params = json.load(file)
    return params


def category_into_int(
    df: pd.DataFrame, column_name: str, new_column_name: str = None
) -> pd.DataFrame:
    """
    Converting the content of column_name  section into integers.

    :param df:
    :param column_name:
    :param new_column_name:
    :return:
    """
    if new_column_name is None:
        new_column_name = column_name

    category_values = df[column_name].unique()
    category_dict = {}
    for i in range(0, len(category_values)):
        category_dict[category_values[i]] = i

    df[new_column_name] = df[column_name].map(category_dict).astype(int)
    return df


def str_to_int(value: str):
    """
    Scaling and cleaning size of installation.
    :param size:
    :return:
    """
    if type(value) == int:
        return value
    DIGITS = list(map(str, range(10)))
    if "m" == value[-1].lower():
        x = value[:-1]
        x = float(x) * 1000000
        return x
    elif "k" == value[-1].lower():
        x = value[:-1]
        x = float(x) * 1000
        return x
    elif value[-1] in DIGITS:
        return float(value)
    else:
        return None  # was None but linters can't accept it


def transform_csv_digits(value: str):
    try:
        return int(value[:-1].replace(",", ""))
    except Exception:
        return None


def bin_category_into_int(negative_class_name: str):
    def wrapper(value: str) -> int:
        if value == negative_class_name:
            return 0
        else:
            return 1

    return wrapper


def price_clean(price: str) -> float:
    if price == "0":
        return 0
    else:
        try:
            return float(price[1:])
        except Exception:
            return 0
