import MetaTrader5 as mt5
import pandas as pd
import os

# Initialize MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# Define the symbol and time frames
symbol = "ETHUSD"
timeframes = {
    '1H': mt5.TIMEFRAME_H1,
    '30M': mt5.TIMEFRAME_M30,
    '15M': mt5.TIMEFRAME_M15,
    '4H': mt5.TIMEFRAME_H4,
    'D1': mt5.TIMEFRAME_D1
}
start_date = "2024-01-01"
end_date = "2024-07-01"

# Convert dates to datetime format
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Fetch and save data for each timeframe
for tf_name, tf in timeframes.items():
    # Fetch historical data
    rates = mt5.copy_rates_range(symbol, tf, start_date, end_date)

    # Convert to DataFrame
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate Change(Pips) and Change(%)
    data['Change(Pips)'] = data['close'].diff() * 100  # Assuming 1 pip = 0.01
    data['Change(%)'] = data['close'].pct_change() * 100

    # Define file path
    file_path = f'data/{symbol}_{tf_name}.csv'

    # Save to CSV
    data.to_csv(file_path, index=False)

    print(f"Data saved to {file_path}")

# Shutdown MetaTrader 5
mt5.shutdown()
