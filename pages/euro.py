import streamlit as st

if st.session_state.get("currency") != "EUR":
    st.session_state.pop("prediction", None)
st.session_state.currency = "EUR"

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


# Тут підключається графік із charts.py.
# Назву create_chart замініть на назву функції учасника №4.
# from charts import create_chart

chart_place = st.empty()
chart_place.info("Тут буде графік курсу EUR")

# Коли функція буде готова:
# chart = create_chart(...)
# chart_place.plotly_chart(chart)

st.divider()

if "balance" not in st.session_state:
    st.session_state.balance = 1000

st.metric("Баланс (грн)", f"{st.session_state.balance:.2f}")

stake = st.number_input(
    "Сума ставки (грн)",
    min_value=0.0,
    value=0.0,
    step=10.0,
    key="stake",
)

column1, column2 = st.columns(2)

with column1:
    button_up = st.button("Виросте", key="up_btn", width="stretch")

with column2:
    button_not_up = st.button("Не виросте", key="not_up_btn", width="stretch")

if button_up or button_not_up:
    if not 0 < stake <= st.session_state.balance:
        st.error("Ставка має бути більшою за нуль і не перевищувати баланс.")
    else:
        if button_up:
            st.session_state.prediction = "Виросте"
        else:
            st.session_state.prediction = "Не виросте"

if "prediction" in st.session_state:
    st.write("Прогноз:", st.session_state.prediction)
    st.write("Ставка:", stake, "грн")

if st.button("Back", key="back_btn"):
    st.switch_page("app.py")



