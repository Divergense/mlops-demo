import pandas as pd
from typing import Tuple


def read_process_write(func, *, input: str, output: Tuple[str]):
    df = pd.read_csv(input)
    results = func(df)
    if len(results) != len(output):
        raise ValueError(
            "Number of generated files doesn't correspond to number of output files. "
            + f"Generated files: {len(results)}; given output file names: {len(output)}"
        )

    for i in range(len(results)):
        results[i].to_csv(output[i], index=False)
