import requests
import json
from datetime import datetime

# Konfigurasi
SYMBOL = "BTCUSDT"
INTERVAL = "1h"  # Kita gunakan timeframe 1 jam untuk RSI yang lebih stabil

def get_crypto_data():
    # Mengambil data kline/candlestick untuk menghitung RSI
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=20"
    response = requests.get(url)
    data = response.json()
    
    # Ambil harga penutupan (closing prices)
    closes = [float(candle[4]) for candle in data]
    return closes

def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return 50  # Netral jika data kurang
    
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def generate_signal(rsi, price):
    if rsi <= 30:
        return "🔥 STRONG BUY (Oversold)"
    elif rsi >= 70:
        return "⚠️ STRONG SELL (Overbought)"
    elif rsi > 50:
        return "Kecenderungan NAIK (Wait)"
    else:
        return "Kecenderungan TURUN (Wait)"

def main():
    try:
        prices = get_crypto_data()
        current_price = prices[-1]
        rsi_value = calculate_rsi(prices)
        signal = generate_signal(rsi_value, current_price)
        
        # Data yang akan dikirim ke website
        output = {
            "price": f"{current_price:,}",
            "rsi": rsi_value,
            "signal": signal,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("data.json", "w") as f:
            json.dump(output, f)
            
        print(f"Update Berhasil: BTC ${current_price} | RSI: {rsi_value}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
