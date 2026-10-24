import tkinter
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import json


base_url = 'https://api.coingecko.com/api/v3'
api = 'CG-LGbLjNCxJ7qcSKsR6tjaZAvr'   # <-- эта строка обязательна

headers = {
    'accept': 'application/json',
    'x-cg-demo-api-key': api
}

url = f'{base_url}/simple/price'
params = {
    'ids': 'bitcoin,solana',
    'vs_currencies': 'usd'
}

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    print('Данные успешно получены')
    print(f"Bitcoin: ${data['bitcoin']['usd']:.2f}")
    print(f"Solana: ${data['solana']['usd']:.2f}")

except requests.exceptions.HTTPError as e:
    print(f'Ошибка HTTP: {e}')







def update_label(event):
    select_text = kripto_combobox.get()
    label.config(text=select_text)





window = Tk()
window.title('Текущие курсы криптовалют')
window.geometry('338x330')



kriptovaluta = {
    'BTC' : 'Bitcoin',
    'ETH' : 'Ethereum',
    'USDT' : 'Tether',
    'BNB' : 'Binance Coin',
    'XRP' : 'Ripple',
    'USDC' : 'USD Coin',
    'SOL' : 'Solana'
}



Label(text='Популярные криптовалюты', font=('Helvetica', 10)).pack()
label = Label(textvariable=update_label, font=('Arial', 12, 'bold'))
label.pack()



kripto_combobox = ttk.Combobox(window, values= list(kriptovaluta), state='readonly')
kripto_combobox.current(0)
kripto_combobox.bind('<<ComboboxSelected>>')
kripto_combobox.pack()






window.mainloop()