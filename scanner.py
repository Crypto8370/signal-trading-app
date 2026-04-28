import requests
import json
import os
from datetime import datetime

# Konfigurasi Scalping M1
SYMBOL = "BTCUSDT"
INTERVAL = "1m" 
RSI_PERIOD = 14

def get_data():
    try:
        # Mengambil data candle dari Binance
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return [float(c[4]) for c in response.json()]
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return None

def calculate_rsi(prices):
    if not prices or len(prices) < RSI_PERIOD: return 50
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gain = [d if d > 0 else 0 for d in deltas]
    loss = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gain[-RSI_PERIOD:]) / RSI_PERIOD
    avg_loss = sum(loss[-RSI_PERIOD:]) / RSI_PERIOD
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1+rs)), 2)

def send_telegram(msg):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
            requests.get(url, timeout=10)
        except:
            print("Gagal kirim notifikasi Telegram")

# Proses Utama
prices = get_data()
if prices:
    current_price = prices[-1]
    rsi_val = calculate_rsi(prices)
    
    signal = "WAITING"
    if rsi_val <= 60:
        signal = "🔥 BUY (M1)"
        send_telegram(f"🚀 BTC M1 BUY\nHarga: ${current_price}\nRSI: {rsi_val}")
    elif rsi_val >= 70:
        signal = "⚠️ SELL (M1)"
        send_telegram(f"🔻 BTC M1 SELL\nHarga: ${current_price}\nRSI: {rsi_val}")

    # Update data untuk Dashboard
    output = {
        "price": f"{current_price:,}",
        "rsi": rsi_val,
        "signal": signal,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("data.json", "w") as f:
        json.dump(output, f)
    
    print(f"Berhasil Update: {current_price} | RSI: {rsi_val}")
else:
    print("Robot berhenti karena gagal koneksi ke Binance.")
