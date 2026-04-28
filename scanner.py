import requests
import json
from datetime import datetime

# === KONFIGURASI TELEGRAM ===
TOKEN = "8690136774:AAE6a8xPxqrR9g7F0qQifZ71FIspnjqWnTA"
CHAT_ID = "6227179398"
# ============================

SYMBOL = "BTCUSDT"
INTERVAL = "1h"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=10)
    except:
        print("Gagal kirim Telegram")

def get_crypto_data():
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=20"
        response = requests.get(url, timeout=10)
        return [float(candle[4]) for candle in response.json()]
    except:
        return None

def calculate_rsi(prices, period=14):
    if not prices or len(prices) < period: return 50
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas]; losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[-period:]) / period; avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def main():
    prices = get_crypto_data()
    if prices:
        current_price = prices[-1]
        rsi_val = calculate_rsi(prices)
        
        signal = "WAITING"
        if rsi_val <= 30: signal = "🔥 BUY (Oversold)"
        elif rsi_val >= 70: signal = "⚠️ SELL (Overbought)"
        
        # Kirim pesan jika ada sinyal BUY atau SELL
        if "BUY" in signal or "SELL" in signal:
            pesan = f"--- SINYAL {SYMBOL} ---\nSinyal: {signal}\nHarga: ${current_price:,}\nRSI: {rsi_val}"
            send_telegram(pesan)

        output = {
            "price": f"{current_price:,}",
            "rsi": rsi_val,
            "signal": signal,
            "last_update": datetime.now().strftime("%m-%d %H:%M")
        }
        with open("data.json", "w") as f:
            json.dump(output, f)
        print("Update & Notifikasi Selesai")

if __name__ == "__main__":
    main()
