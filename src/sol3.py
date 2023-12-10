from dataclasses import dataclass, field
import datetime
import random
import pandas as pd
from datetime import timedelta
from sol2 import Meter, generate_meters
from utils import list_of_dc_to_df


@dataclass
class MockData:
    meter_id: int
    date: datetime.date
    kwh: float = field(default_factory=lambda: random.uniform(0, 2000))


def get_date(start, delta):
    return start + timedelta(days=delta)


def generate_mock_data(meters: list[Meter], start_date: datetime.date, duration: int):
    out = []
    meter_ids = [m.meter_id for m in meters]
    for m in meter_ids:
        out.extend([MockData(m, get_date(start_date, i)) for i in range(duration)])
    return out


if __name__ == "__main__":
    n = 3
    meters = generate_meters(n)
    print(meters)
    mock_data = generate_mock_data(
        meters, start_date=datetime.date.today(), duration=10
    )
    print(mock_data)
    print(len(mock_data))
    print(list_of_dc_to_df(mock_data))
