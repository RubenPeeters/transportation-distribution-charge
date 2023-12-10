import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from timeit import timeit

from sol2 import generate_meters
from sol3 import generate_mock_data
from utils import list_of_dc_to_df
import pprint


# I don't see how I can calculate without using the rate_table. Added as additional parameter.
def transportation_cost_table(
    meters: pd.DataFrame, ft: pd.DataFrame, rt: pd.DataFrame
) -> pd.DataFrame:
    merged_ml_ft = meters.merge(ft, on="meter_id", how="right")
    merged_ml_ft_rt = merged_ml_ft.merge(rt, on=["exit_zone", "date"], how="inner")
    merged_ml_ft_rt["aq_max_kwh"] = merged_ml_ft_rt["aq_max_kwh"].fillna(value=np.inf)
    merged_ml_ft_rt = merged_ml_ft_rt[
        merged_ml_ft_rt["rate_p_per_kwh"].between(
            merged_ml_ft_rt["aq_min_kwh"],
            merged_ml_ft_rt["aq_max_kwh"],
            inclusive="left",
        )
    ]
    merged_ml_ft_rt["cost_per_day"] = (
        merged_ml_ft_rt["kwh"] * merged_ml_ft_rt["rate_p_per_kwh"]
    )
    total_cost = merged_ml_ft_rt[["meter_id", "cost_per_day"]].groupby("meter_id").sum()
    total_cost["cost_per_day (p)"] = total_cost["cost_per_day"] / 100
    total_consumption = merged_ml_ft_rt[["meter_id", "kwh"]].groupby("meter_id").sum()
    merged_tc_tc = total_cost.merge(total_consumption, on="meter_id").reset_index()
    out = (
        merged_tc_tc.drop("cost_per_day", axis=1)
        .rename(
            columns={
                "cost_per_day (p)": "Total Cost (£)",
                "meter_id": "Meter ID",
                "kwh": "Total Estimated Consumption (kWh)",
            }
        )
        .round(2)
    )
    return out


if __name__ == "__main__":
    n = 3
    start_date = (2020, 6, 1)
    duration = 365
    top_dir = Path.cwd()

    # get given rate table
    sheets = pd.read_excel(top_dir / "data" / "gorilla_test_data.xlsx", sheet_name=None)
    rt = sheets["rate_table"]

    # get list of meters
    meters = generate_meters(n)
    mock_meters = list_of_dc_to_df(meters)
    pprint.pprint(meters)

    # get forecast table
    mock_data = generate_mock_data(
        meters, start_date=datetime.date(*start_date), duration=duration
    )
    mock_ft = list_of_dc_to_df(mock_data)
    mock_ft["date"] = mock_ft["date"].astype("datetime64[ns]")

    # calculate tranportation cost table
    print(transportation_cost_table(meters=mock_meters, ft=mock_ft, rt=rt))

    # benchmarking
    meter_sizes = [1, 10, 100, 1000, 10000, 100000]
    durations = [1, 7, 31, 365, 730, 3652]

    for m in meter_sizes:
        meters = generate_meters(m)
        mock_meters = list_of_dc_to_df(meters)
        for d in durations:
            mock_data = generate_mock_data(
                meters, start_date=datetime.date(*start_date), duration=duration
            )
            mock_ft = list_of_dc_to_df(mock_data)
            mock_ft["date"] = mock_ft["date"].astype("datetime64[ns]")
            t = timeit(
                "transportation_cost_table(meters=mock_meters, ft=mock_ft, rt=rt)",
                setup="from __main__ import transportation_cost_table",
                number=1,
                globals={"mock_meters": mock_meters, "mock_ft": mock_ft, "rt": rt},
            )
            print(f"Execution with variables {m=} {d=} took {t:.6f}s")
