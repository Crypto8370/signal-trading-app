import requests
import json

# 1. Ambil data harga dari Binance
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

# 2. Logika Sinyal Sederhana (Contoh: Dummy Logic)
# Nanti kita bisa ganti dengan RSI, EMA, atau strategi DCA Anda
def generate_signal(price):
    if price < 60000: # Contoh logika sederhana
        return "BUY"
    elif price > 80000:
        return "SELL"
    else:
        return "WAITING"

# 3. Simpan hasil ke file JSON agar bisa dibaca oleh Website
price = get_price()
signal = generate_signal(price)

status = {
    "price": price,
    "signal": signal,
    "last_update": "Terakhir diperbarui: Real-time dari Python"
}

with open('data.json', 'w') as f:
    json.dump(status, f)

print(f"Berhasil! Harga: {price}, Sinyal: {signal}")
