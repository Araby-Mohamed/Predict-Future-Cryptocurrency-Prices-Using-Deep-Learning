import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

st.title("Bitcoin Price Predictor App")

stock = "BTC-USD"
end = datetime.now()
start = datetime(end.year-10, end.month, end.day)

stock = st.text_input("Enter the stock here", stock)

bit_coin_data = yf.download(stock, start, end)

model = load_model("predicting_stock_prices_use_rnn_algorithm.ipynb.keras")
st.subheader("BTC-USD Data")
st.write(bit_coin_data)

splitting_len = int(len(bit_coin_data) * 0.9)
x_test = pd.DataFrame(bit_coin_data.Close[splitting_len:])

st.subheader('Original Close Price')
figsize = (15, 6)
fig = plt.figure(figsize=figsize)
plt.plot(bit_coin_data.Close, 'b')
st.pyplot(fig)

st.subheader("Test Close Price")
st.write(x_test)

st.subheader('Test Close Price')
figsize = (15, 6)
fig = plt.figure(figsize=figsize)
plt.plot(x_test, 'b')
st.pyplot(fig)

# preprocess the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(x_test[['Close']].values)

x_data = []
y_data = []
for i in range(100, len(scaled_data)):
    x_data.append(scaled_data[i-100:i])
    y_data.append(scaled_data[i])

x_data, y_data = np.array(x_data), np.array(y_data)

predictions = model.predict(x_data)
inv_pre = scaler.inverse_transform(predictions)
inv_y_test = scaler.inverse_transform(y_data)

ploting_data = pd.DataFrame(
    {
        'original_test_data': inv_y_test.reshape(-1),
        'predictions': inv_pre.reshape(-1)
    },
    index=bit_coin_data.index[splitting_len+100:]
)

st.subheader("Original values vs Predicted values")
st.write(ploting_data)

st.subheader('Original Close Price vs Predicted Close price')
fig = plt.figure(figsize=(15, 6))
plt.plot()
plt.plot(pd.concat([bit_coin_data.Close[:splitting_len+100], ploting_data], axis=0))
plt.legend(["Data- not used", "Original Test data", "Predicted Test data"])
st.pyplot(fig)

st.subheader("Future Price values")

last_100 = bit_coin_data[['Close']].tail(100)
last_100 = scaler.fit_transform(last_100['Close'].values.reshape(-1, 1)).reshape(1, -1, 1)
prev_100 = np.copy(last_100).tolist()

def predict_future(no_of_days, prev_100):
    future_predictions = []
    for i in range(int(no_of_days)):
        next_day = model.predict(prev_100).tolist()
        prev_1
