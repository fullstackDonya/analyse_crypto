import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Get the current date in the 'YYYY-MM-DD' format
current_date = datetime.now().strftime('%Y-%m-%d')

def get_crypto_data(symbols, start_date, end_date):
    crypto_data = pd.DataFrame()
    for symbol in symbols:
        try:
            crypto_ticker = yf.Ticker(symbol)
            data = crypto_ticker.history(start=start_date, end=end_date)['Close']
            if not data.empty:
                crypto_data[symbol] = data
            else:
                print(f"No data available for {symbol} in the specified date range.")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return crypto_data

def analyze_crypto_value(crypto_data):
    crypto_data['Average_Daily_Return'] = crypto_data.pct_change().mean(axis=1)
    sorted_cryptos = crypto_data.sort_values(by='Average_Daily_Return', ascending=True)
    return sorted_cryptos

if __name__ == "__main__":
    crypto_symbols = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'ADA-USD', 'DOT-USD', 'BNB-USD', 'DOGE-USD', 'SOL-USD', 'LINK-USD', 'OMG-USD', 'IOTA-USD', 'NEO-USD', 'XLM-USD', 'TRX-USD']
    start_date = '2019-01-01'
    # Use current_date as the end_date
    end_date = current_date

    crypto_data = get_crypto_data(crypto_symbols, start_date, end_date)

    sorted_cryptos = analyze_crypto_value(crypto_data)

    print("Crypto-monnaies classées par ordre croissant de rendement moyen quotidien :")
    print(sorted_cryptos)

    # Data Visualization
    plt.figure(figsize=(12, 6))

    for crypto in crypto_symbols:
        if crypto in crypto_data.columns:
            plt.plot(crypto_data.index, crypto_data[crypto], label=crypto)

    plt.title('Analyse des Crypto-monnaies')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.legend()
    plt.show()