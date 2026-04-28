import requests
import json
import os

# Konfigurasi Scalping
SYMBOL = "BTCUSDT"
INTERVAL = "1m"  # Menggunakan timeframe 1 menit
RSI_PERIOD = 14

def get_data():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=100"
    data = requests.get(url).json()
    return [float(c[4]) for c in data]

def calculate_rsi(prices):
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
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
        requests.get(url)

prices = get_data()
current_price = prices[-1]
rsi = calculate_rsi(prices)

signal = "WAITING / NEUTRAL"
if rsi <= 30:
    signal = "🔥 SCALP BUY (Oversold)"
    send_telegram(f"🚀 BTC M1 BUY SIGNAL\nPrice: ${current_price}\nRSI: {rsi}")
elif rsi >= 70:
    signal = "⚠️ SCALP SELL (Overbought)"
    send_telegram(f"🔻 BTC M1 SELL SIGNAL\nPrice: ${current_price}\nRSI: {rsi}")

# Simpan ke data.json untuk Dashboard
output = {
    "price": f"{current_price:,}",
    "rsi": rsi,
    "signal": signal,
    "last_update": requests.get("https://worldtimeapi.org/api/timezone/Asia/Jakarta").json()['datetime'][:19].replace("T", " ")
}

with open("data.json", "w") as f:
    json.dump(output, f)

print(f"Scalping Scan Selesai: {current_price} | RSI: {rsi}")
