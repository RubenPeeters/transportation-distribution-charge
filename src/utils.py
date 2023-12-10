import pandas as pd
import dataclasses


def list_of_dc_to_df(dc):
    return pd.DataFrame.from_records([dataclasses.asdict(c) for c in dc])
