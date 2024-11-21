import requests
from decimal import Decimal
import pandas as pd
from datetime import datetime
import schedule
import time

# Global DataFrame to store prices
price_data = pd.DataFrame()

def get_coin_prices(coin_ids, currency='usd'):
    """
    Fetch current prices of specified coins in a given currency.
    :param coin_ids: List of coin IDs (e.g., ['dogecoin', 'shiba-inu']).
    :param currency: The target currency (default: 'usd').
    :return: Dictionary of coin prices.
    """
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(coin_ids),  # Join the coin IDs into a comma-separated string
        'vs_currencies': currency  # Target currency
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad response
        data = response.json()  # Parse JSON response
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}



def fetch_and_store_prices():
    global price_data
    coins = ['dogecoin', 'shiba-inu', 'pepe']
    currency = 'usd'
    prices = get_coin_prices(coins, currency)

    if prices:
        timestamp = datetime.now()
        for coin, info in prices.items():
            formatted_price = float(info[currency])
            # Add to DataFrame
            price_data = price_data._append({'timestamp': timestamp, 'coin': coin, 'price': formatted_price}, ignore_index=True)
        print(f"Data stored at {timestamp}")
    else:
        print("Failed to fetch prices.")

def analyze_trends():
    global price_data
    if price_data.empty:
        print("No data to analyze.")
        return

    for coin in price_data['coin'].unique():
        coin_data = price_data[price_data['coin'] == coin]

        # Calculate percentage change
        price_data['pct_change'] = coin_data['price'].pct_change() * 100

        # Calculate simple moving average
        price_data['moving_avg'] = coin_data['price'].rolling(window=5).mean()

        # Print analysis
        print(f"Trend for {coin.capitalize()}:")
        print(price_data.tail(5))  # Last 5 data points


# Example Usage
if __name__ == '__main__':
    coins = ['dogecoin', 'shiba-inu', 'pepe']
    currency = 'usd'
    prices = get_coin_prices(coins, currency)

    if prices:
        print("Current Prices:")
        for coin, info in prices.items():
            price = Decimal(info[currency])
            print(f"{coin.capitalize()}: {price} {currency.upper()}")


# Schedule the task to run every minute
    schedule.every(1).minute.do(fetch_and_store_prices)

    print("Tracking prices... Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
