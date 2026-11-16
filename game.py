import random
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CURRENCY_FILES = {"USD": "usd.csv", "EUR": "eur.csv"}
DURATIONS = (7, 14, 30)
HISTORY_DAYS = 30          # скільки днів історії показуємо на графіку
PERIOD_START = pd.Timestamp("2020-01-01")
PERIOD_END = pd.Timestamp("2025-12-31")


def load_rates(currency):
    """Зчитує курс валюти з CSV і повертає очищені дані."""
    if currency not in CURRENCY_FILES:
        raise ValueError(f"Невідома валюта: {currency}")
    df = pd.read_csv(DATA_DIR / CURRENCY_FILES[currency])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return clean_rates(df)
  
