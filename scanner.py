import requests
import json
from datetime import datetime

# Konfigurasi
SYMBOL = "BTCUSDT"
INTERVAL = "1h"

def get_crypto_data():
    try:
        # Timeout 10 detik agar robot tidak "hang" jika internet lambat
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=20"
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Cek jika ada error HTTP
        data = response.json()
        
        closes = [float(candle[4]) for candle in data]
        return closes
    except Exception as e:
        print(f"Gagal mengambil data dari Binance: {e}")
        return None

def calculate_rsi(prices, period=14):
    try:
        if not prices or len(prices) < period:
            return 50
        
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
    except:
        return 50

def generate_signal(rsi):
    if rsi <= 30:
        return "🔥 STRONG BUY (Oversold)"
    elif rsi >= 70:
        return "⚠️ STRONG SELL (Overbought)"
    elif rsi > 50:
        return "Trend NAIK (Wait)"
    else:
        return "Trend TURUN (Wait)"

def main():
    # 1. Siapkan data default jika terjadi error
    output = {
        "price": "Dalam Pembaruan...",
        "rsi": "--",
        "signal": "Menghubungkan ke Server...",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 2. Coba ambil data asli
    prices = get_crypto_data()
    
    if prices:
        current_price = prices[-1]
        rsi_value = calculate_rsi(prices)
        signal = generate_signal(rsi_value)
        
        output = {
            "price": f"{current_price:,}",
            "rsi": rsi_value,
            "signal": signal,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    # 3. Selalu simpan file, baik data asli maupun data "Menunggu"
    try:
        with open("data.json", "w") as f:
            json.dump(output, f)
        print(f"Update Selesai: {output['signal']}")
    except Exception as e:
        print(f"Gagal menulis file: {e}")

if __name__ == "__main__":
    main()
