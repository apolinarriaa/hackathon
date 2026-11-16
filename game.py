import random
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CURRENCY_FILES = {"USD": "usd.csv", "EUR": "eur.csv"}
DURATIONS = (7, 14, 30)
HISTORY_DAYS = 30          # скільки днів історії показуємо на графіку
PERIOD_START = pd.Timestamp("2020-01-01")
PERIOD_END = pd.Timestamp("2025-12-31")
