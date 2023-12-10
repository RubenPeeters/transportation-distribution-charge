from dataclasses import dataclass, field
import random

from utils import list_of_dc_to_df

VALID_EXITS = [
    "EA1",
    "EA2",
    "EA3",
    "EA4",
    "EM1",
    "EM2",
    "EM3",
    "EM4",
    "LC",
    "LO",
    "LS",
    "LT",
    "LW",
    "NE1",
    "NE2",
    "NE3",
    "NO1",
    "NO2",
    "NT1",
    "NT2",
    "NT3",
    "NW1",
    "NW2",
    "SC1",
    "SC2",
    "SC4",
    "SE1",
    "SE2",
    "SO1",
    "SO2",
    "SW1",
    "SW2",
    "SW3",
    "WA1",
    "WA2",
    "WM1",
    "WM2",
    "WM3",
]


@dataclass
class Meter:
    meter_id: int = field(default_factory=lambda: random.randint(10000000, 99999999))
    aq_kwh: int = field(
        default_factory=lambda: random.randint(0, 200000)
    )  # 200000 so the chance to get < 100000 and > 100000 is the same, demonstration purposes
    exit_zone: str = field(default_factory=lambda: random.choice(VALID_EXITS))


def generate_meters(n):
    return [Meter() for _ in range(n)]


if __name__ == "__main__":
    n = 10
    meters = generate_meters(n)
    print(meters)
    print(len(meters))
    print(list_of_dc_to_df(meters))
