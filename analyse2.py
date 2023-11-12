import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mplcursors
import matplotlib.dates as mdates  # Import the module for formatting dates

# Get the current date in the 'YYYY-MM-DD' format
current_date = datetime.now().strftime('%Y-%m-%d')

def get_crypto_data(symbols, start_date, end_date):
    crypto_data = pd.DataFrame()
    for symbol in symbols:
        try:
            crypto_ticker = yf.Ticker(symbol)
            data = crypto_ticker.history(period='1d')  # Retrieve only the most recent data
            if not data.empty:
                crypto_data[symbol] = data['Close']
            else:
                print(f"No data available for {symbol}.")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return crypto_data

def analyze_crypto_value(crypto_data):
    crypto_data['Average_Daily_Return'] = crypto_data.pct_change().mean(axis=1)
    sorted_cryptos = crypto_data.sort_values(by='Average_Daily_Return', ascending=True)
    return sorted_cryptos

def estimate_trend(row, threshold=0.01):
    if row['Average_Daily_Return'] > threshold:
        return 'Hausse'
    elif row['Average_Daily_Return'] < -threshold:
        return 'Baisse'
    else:
        return 'Stable'

def estimate_future_trend(row, future_data, threshold=0.01):
    # Check if the date is in the future_data
    if row.name in future_data.index and 'Tendance' in future_data.columns:
        if future_data.at[row.name, 'Tendance'] == 'Hausse prévue':
            return 'Hausse prévue'
        elif future_data.at[row.name, 'Tendance'] == 'Baisse prévue':
            return 'Baisse prévue'
        else:
            return 'Stable prévue'
    else:
        return 'Non disponible'

# Function to handle cursor hovering over data points
def on_hover(sel):
    index = sel.target[0]
    line = sel.artist
    label = line.get_label()

    # Create a new figure for detailed view
    plt.figure(figsize=(12, 8))  # Increase figure size

    # Plot historical values
    plt.plot(crypto_data.index, crypto_data[label], label=f"{label} (Historical)", alpha=0.7)

    # Plot future values
    if label in future_data.columns:
        future_values = future_data[label].loc[crypto_data.index[-1]:]
        plt.plot(future_values.index, future_values, linestyle='--', label=f"{label} (Future)", alpha=0.7)

    plt.title(f'Detailed View for {label}')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.xticks(rotation=60)  # Increase rotation angle

    # Format x-axis dates with months, days, and hours
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    plt.show()
if __name__ == "__main__":
    crypto_symbols = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'ADA-USD', 'DOT-USD', 'BNB-USD', 'DOGE-USD', 'SOL-USD', 'LINK-USD', 'OMG-USD', 'IOTA-USD', 'NEO-USD', 'XLM-USD', 'TRX-USD']
    start_date = '2019-01-01'
    # Use current_date as the end_date
    end_date = current_date

    crypto_data = get_crypto_data(crypto_symbols, start_date, end_date)

    sorted_cryptos = analyze_crypto_value(crypto_data)

    crypto_data['Tendance'] = crypto_data.apply(estimate_trend, axis=1)



    # Estimer la tendance future pour les jours à venir
    future_dates = pd.date_range(pd.to_datetime(end_date), pd.to_datetime(end_date) + timedelta(days=5))
    future_data = pd.DataFrame(index=future_dates, columns=crypto_symbols)

    for crypto in crypto_symbols:
        if crypto in crypto_data.columns:
            # Utiliser la tendance actuelle pour estimer la tendance future
            last_historical_value = crypto_data[crypto].iloc[-1]  # Get the last historical value
            future_data[crypto] = estimate_future_trend(crypto_data.loc[crypto_data.index[-1]], future_data)


    print("Crypto-monnaies classées par ordre croissant de rendement moyen quotidien :")
    print(sorted_cryptos)

    print("Estimation de la tendance pour les jours à venir :")
    print(future_data)
    
    # Data Visualization
    plt.figure(figsize=(12, 7))
    # Plot historical values
    for crypto in crypto_symbols:
        if crypto in crypto_data.columns:
            line, = plt.plot(crypto_data.index, crypto_data[crypto], label=f"{crypto} (Historical)", alpha=0.7)

    # Plot future values
    for crypto in crypto_symbols:
        if crypto in future_data.columns:
            plt.plot(future_data.index, future_data[crypto], linestyle='--', label=f"{crypto} (Future)", alpha=0.7)

    plt.title('Analyse des Crypto-monnaies')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.legend()

    # Enable cursor hover
    mplcursors.cursor(hover=True).connect("add", on_hover)

    plt.yscale('log')  # Set y-axis to log scale
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add grid lines
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tick_params(axis='both', labelsize=10)  # Increase tick label font size
    plt.show()