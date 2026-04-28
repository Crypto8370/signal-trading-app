import requests
import json
import datetime

def get_price():
    try:
        # Mengambil harga BTC terbaru dari Binance
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url)
        data = response.json()
        return float(data['price'])
    except:
        return 0.0

def generate_signal(price):
    # Contoh Logika: Jika harga di bawah 65000 BUY, di atas 80000 SELL
    # Anda bisa merubah angka ini nanti sesuai strategi Anda
    if price > 0 and price < 65000:
        return '<span style="color: #00ff00;">BUY</span>'
    elif price > 80000:
        return '<span style="color: #ff0000;">SELL</span>'
    else:
        return '<span style="color: #ffaa00;">WAITING / NEUTRAL</span>'

# Eksekusi program
price = get_price()
signal = generate_signal(price)
waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Format data untuk ditampilkan di website
status = {
    "price": f"{price:,.2f}",
    "signal": signal,
    "last_update": waktu
}

# Menyimpan hasil ke file data.json
with open('data.json', 'w') as f:
    json.dump(status, f)

print(f"Update Berhasil: {price} - {signal}")
