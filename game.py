import random
from pathlib import Path
import pandas as pd
import streamlit as st
DATA_DIR = Path(__file__).parent / "data"
CURRENCY_FILES = {"USD": "usd.csv", "EUR": "eur.csv"}
DURATIONS = (7, 14, 30)
HISTORY_DAYS = 30 # скільки днів до старту показуємо на графіку
PERIOD_START = pd.Timestamp("2020-01-01")
PERIOD_END = pd.Timestamp("2025-12-31")
# Стан гри зберігається між натисканнями кнопок
def get_state():
    return st.session_state.setdefault("game_state", {})


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


def start_game(currency, duration_days, rng=random):
    """Починає гру: зчитує курси, обирає випадковий період, ставить день 0."""
    if duration_days not in DURATIONS:
        raise ValueError(f"Тривалість має бути однією з {DURATIONS}")
    rates = load_rates(currency)
    get_state().clear()
    get_state().update({
        "currency": currency,
        "duration": duration_days,
        "rates": rates,
        "start_index": choose_start(rates, duration_days, rng),
        "day": 0,
    })
    return get_current_day()


def _require_game():
    if not get_state():
        raise RuntimeError("Гру ще не розпочато — спершу виклич start_game()")

def _current_index():
    return get_state()["start_index"] + get_state()["day"]


def is_finished():
    _require_game()
    return get_state()["day"] >= get_state()["duration"]


def get_current_day():
    """Поточна дата, курс, номер раунду та ознака завершення гри."""
    _require_game()
    row = get_state()["rates"].loc[_current_index()]
    return {
        "currency": get_state()["currency"],
        "date": row["date"],
        "rate": float(row["rate"]),
        "round": min(get_state()["day"] + 1, get_state()["duration"]),
        "total_rounds": get_state()["duration"],
        "finished": is_finished(),
    }

def next_day():
    """Відкриває наступний день і повертає старий та новий курс."""
    if is_finished():
        raise ValueError("Гру вже завершено.")
    old_rate = get_current_day()["rate"]
    get_state()["day"] += 1
    new_rate = get_current_day()["rate"]
    return old_rate, new_rate


def get_history():
    """Повертає лише історію до поточного відкритого дня."""
    _require_game()
    first = max(0, get_state()["start_index"] - HISTORY_DAYS)
    last = _current_index() + 1
    return get_state()["rates"].iloc[first:last].copy()

if __name__ == "__main__":
    for code in CURRENCY_FILES:
        raw = pd.read_csv(DATA_DIR / CURRENCY_FILES[code], parse_dates=["date"])
        print(code, "перевірка:", check_dates(raw))

    print("Старт:", start_game("USD", 7))
    print("Історія для графіка:", len(get_history()), "днів")
    while not is_finished():
        print(next_day())
    print("Кінець:", get_current_day())
