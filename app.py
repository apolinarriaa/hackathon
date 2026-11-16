import streamlit as st

st.markdown(
    "<h1 style='text-align: center;'>Choose the currency</h1>",
    unsafe_allow_html=True)
st.markdown("""
<style>
    div.stButton > button {
        height: 100px;
    }

    div.stButton > button p {
        font-size: 30px;
    }
</style>
""", unsafe_allow_html=True)

column1, column2 = st.columns(2)

with column1:
    button_usdt = st.button("USD", width="stretch")

with column2:
    button_eur = st.button("EUR", width="stretch")

balance = st.slider(
    "Вибери баланс (грн)",
    min_value=500,
    max_value=10000,
    value=1000,
    step=100,
)

st.session_state.balance = balance

duration_days = st.selectbox(
    "Тривалість гри (днів)",
    options=[7, 14, 30],
    index=[7, 14, 30].index(st.session_state.get("duration_days", 7)),
)
st.session_state.duration_days = duration_days

if button_usdt:
    st.switch_page("pages/usd.py")
if button_eur:
    st.switch_page("pages/euro.py")
