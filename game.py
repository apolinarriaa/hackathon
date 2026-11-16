import random
from pathlib import Path
import pandas as pd
DATA_DIR = Path(__file__).parent / "data"
CURRENCY_FILES = {"USD": "usd.csv", "EUR": "eur.csv"}
DURATIONS = (7, 14, 30)
HISTORY_DAYS = 30 # скільки днів до старту показуємо на графіку
PERIOD_START = pd.Timestamp("2020-01-01")
PERIOD_END = pd.Timestamp("2025-12-31")
# Стан гри зберігається між натисканнями кнопок
_state = {}


def load_rates(currency):
  """Зчитує CSV валюти, перетворює дату, сортує й очищає дані."""
  if currency not in CURRENCY_FILES:
  raise ValueError(f"Невідома валюта: {currency}")
  df = pd.read_csv(DATA_DIR / CURRENCY_FILES[currency])
  df["date"] = pd.to_datetime(df["date"])
  df = df.sort_values("date")
  return clean_rates(df)


def check_dates(df):
  """Рахує повтори дат і пропущені календарні дні."""
  duplicates = int(df["date"].duplicated().sum())
  full_range = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
  missing = len(full_range) - df["date"].nunique()
  return {"duplicates": duplicates, "missing": missing}

def clean_rates(df):
  """Прибирає повтори й заповнює пропущені дні останнім відомим курсом."""
  df = df.drop_duplicates(subset="date", keep="last")
  df = df.set_index("date")
  full_range = pd.date_range(df.index.min(), df.index.max(), freq="D")
  df = df.reindex(full_range).ffill()
  df.index.name = "date"
  return df.reset_index()[["date", "rate"]]

def choose_start(rates, duration_days, rng=random):
  """Випадковий старт: є історія для графіка, і всі duration_days + 1 курсів у 2020–2025."""
  dates = rates["date"]
  in_period = rates.index[(dates >= PERIOD_START) & (dates <= PERIOD_END)]
  first = max(in_period[0], HISTORY_DAYS)
  last = in_period[-1] - duration_days # для 7 прогнозів потрібно 8 курсів
  return rng.randint(first, last)
