import click

from src.utility import processing
from src.params_file import PARAMS_FILE
from src.utility.processing import load_json_params
from src.utility.wrappers import read_process_write


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def clean_features(input: str, output: str):
    params = load_json_params(PARAMS_FILE)
    MEDIAN_SIZE = params["MEDIAN_SIZE"]

    def process(df):
        # transform Categories into integers
        df = processing.category_into_int(df, "Category", "Category_c")
        df.drop(labels=["Category"], axis=1, inplace=True)
        # scaling and cleaning size of installation
        df["Size"] = df["Size"].map(processing.str_to_int)  # about 10% will be None
        # filling Size which had NA. WARNING: here is data leakage!
        df["Size"].fillna(
            MEDIAN_SIZE, inplace=True
        )  # better replace with median=13000000
        # cleaning number of installs
        df["Installs"] = df["Installs"].map(processing.transform_csv_digits)
        # converting the paid/free classification types into binary
        df["Type"] = df["Type"].map(processing.bin_category_into_int("Free"))
        # converting of the content rating section into integers
        df = processing.category_into_int(df, "Content Rating")
        # convert genres
        df = processing.category_into_int(df, "Genres", "Genres_c")
        df.drop(labels=["Genres"], axis=1, inplace=True)
        # cleaning prices
        df["Price"] = df["Price"].map(processing.price_clean).astype(float)
        # convert reviews to numeric; may appear NA (pref drop)
        df["Reviews"] = df["Reviews"].map(processing.str_to_int).astype(int)
        # very discussing moment!
        df.dropna(inplace=True)
        return [df]

    read_process_write(process, input=input, output=(output,))


if __name__ == "__main__":
    clean_features()
