import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import yfinance as yf


ticker = "TSLA"
data = yf.download(ticker, start="2010-01-01", end="2023-01-01")


print("Stock Data Overview:")
print(data.head())


data['Date'] = data.index
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day
data = data[['Open', 'High', 'Low', 'Close', 'Volume', 'Year', 'Month', 'Day']]


X = data.drop('Close', axis=1)
y = data['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))


plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label="Actual Prices")
plt.plot(y_pred, label="Predicted Prices")
plt.legend()
plt.title("Actual vs Predicted Stock Prices")
plt.show()
