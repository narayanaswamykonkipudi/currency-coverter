import streamlit as st
import requests


if "history" not in st.session_state:
    st.session_state.history = []


st.title("💱 Currency Converter App")
st.caption("Real-time currency conversion using API")

CURRENCIES = [
    "AUD","BGN","BRL","CAD","CHF","CNY","CZK","DKK","EUR","GBP",
    "HKD","HRK","HUF","IDR","ILS","INR","ISK","JPY","KRW","MXN",
    "MYR","NOK","NZD","PHP","PLN","RON","RUB","SEK","SGD","THB",
    "TRY","USD","ZAR"
]

col1, col2 = st.columns(2)

with col1:
    base = st.selectbox("From Currency", CURRENCIES)

with col2:
    target = st.selectbox("To Currency", CURRENCIES)

amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")


API_KEY = "fca_live_bTXwD55VVruh6o5V91jJBTfN2Qe3USxC3ZYogrtv"
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}"

@st.cache_data
def converter(base):
    url = f"{BASE_URL}&base_currency={base}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()['data']
    except:
        return {}


if st.button("Convert"):
    if base == target:
        st.warning("Select different currencies")

    elif amount == 0:
        st.warning("Please enter amount")

    else:
        with st.spinner("Fetching rates..."):
            data = converter(base)

        if not data:
            st.error("Failed to fetch data")

        elif target in data:
            rate = data[target]
            result = amount * rate

            st.info(f"1 {base} = {rate:.4f} {target}")
            st.success(f"💰 {amount:.2f} {base} = {result:.2f} {target}")

            
            st.session_state.history.append(
                f"{amount:.2f} {base} → {result:.2f} {target}"
            )

        else:
            st.error("Conversion failed")


if st.checkbox("Show all exchange rates"):
    data = converter(base)
    if data:
        st.table(dict(sorted(data.items())))
    else:
        st.error("Failed to fetch data")


st.subheader("📜 Conversion History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(item)
else:
    st.write("No history yet")


if st.button("Clear History"):
    st.session_state.history = []
