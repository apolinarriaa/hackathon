import streamlit as st
from game import get_current_day, get_history, next_day, is_finished
from eur_charts import create_chart

st.markdown("""
<style>
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
    }

    .st-key-back_btn {
        position: fixed;
        left: 24px;
        bottom: 24px;
        width: auto;
        z-index: 1000;
    }
    .st-key-up_btn button {
        background-color: #15803d;
        border-color: #15803d;
        color: white;
    }

    .st-key-not_up_btn button {
        background-color: #b91c1c;
        border-color: #b91c1c;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """<h1 style='text-align: center; margin-bottom: 0; padding-bottom: 0;'>Euro</h1>
    <hr style='margin-top: 6px; margin-bottom: 16px;'>""",
    unsafe_allow_html=True)


if "game_state" not in st.session_state or "betting" not in st.session_state:
    st.info("Спочатку почніть гру на головній сторінці.")
    if st.button("Back", key="back_btn"):
        st.switch_page("app.py")
    st.stop()

current = get_current_day()
if current["currency"] != "EUR":
    st.info("Оберіть EUR на головній сторінці.")
    if st.button("Back", key="back_btn"):
        st.switch_page("app.py")
    st.stop()

betting = st.session_state.betting
st.write(f"Раунд {current['round']} із {current['total_rounds']}")
st.metric("Поточний курс", f"{current['rate']:.4f} грн")
st.plotly_chart(create_chart(get_history()))
st.divider()
st.metric("Баланс (грн)", f"{betting.balance:.2f}")

if betting.history:
    last = betting.history[-1]
    message = f"{last['current_rate']:.4f} → {last['next_rate']:.4f} грн. Результат ставки: {last['result']:+.2f} грн."
    if last["is_correct"]:
        st.success("Правильно! " + message)
    else:
        st.error("Неправильно. " + message)

stake = st.number_input(
    "Сума ставки (грн)",
    min_value=0.0,
    value=0.0,
    step=10.0,
    key="stake",
    disabled=is_finished(),
)

column1, column2 = st.columns(2)
with column1:
    button_up = st.button("Виросте", key="up_btn", width="stretch", disabled=is_finished())
with column2:
    button_not_up = st.button("Не виросте", key="not_up_btn", width="stretch", disabled=is_finished())

if button_up or button_not_up:
    if not betting.validate_bet(stake):
        st.error("Ставка має бути більшою за нуль і не перевищувати баланс.")
    else:
        prediction = "up" if button_up else "not_up"
        old_rate, new_rate = next_day()
        correct = betting.check_prediction(old_rate, new_rate, prediction)
        result = betting.calculate_result(stake, correct)
        st.session_state.balance = betting.update_balance(result)
        betting.add_to_history(stake, prediction, old_rate, new_rate, correct, result)
        st.rerun()

if is_finished():
    st.subheader("Гру завершено")
    profit = betting.balance - betting.initial_balance
    correct_count = sum(item["is_correct"] for item in betting.history)
    st.write(f"Початковий баланс: {betting.initial_balance:.2f} грн")
    st.write(f"Кінцевий баланс: {betting.balance:.2f} грн")
    st.write(f"Прибуток / збиток: {profit:+.2f} грн")
    st.write(f"Прибутковість: {profit / betting.initial_balance:+.1%}")
    st.write(f"Правильних прогнозів: {correct_count} із {len(betting.history)}")
    if st.button("Нова гра"):
        st.session_state.pop("game_state", None)
        st.session_state.pop("betting", None)
        st.switch_page("app.py")

if st.button("Back", key="back_btn"):
    st.switch_page("app.py")
