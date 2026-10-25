import tkinter # Главный модуль библиотеки для создания графического интерфейса
from tkinter import *  # Импорт всех публичных имён tkinter (Tk, Label и т.д.) без префикса
from tkinter import messagebox as mb # Модуль диалоговых окон (сообщения, предупреждения) под псевдонимом mb
from tkinter import ttk # Модуль "тематических" виджетов (Combobox, Progressbar и др.)
import requests # Библиотека для отправки HTTP-запросов к API
import json # Модуль для работы с JSON

base_url = 'https://api.coingecko.com/api/v3' # Базовый адрес CoinGecko API (версия v3)
api = 'CG-LGbLjNCxJ7qcSKsR6tjaZAvr'
headers = {                     # Словарь HTTP-заголовков, отправляемых с запросом
        'accept': 'application/json',  # Клиент ожидает ответ в формате JSON
        'x-cg-demo-api-key': api   # Заголовок с ключом доступа к Demo-тарифу
    }
def exchange():
    """Настройки для обращения к CoinGecko API"""
      # персональный Demo-ключ API
    ticker = kripto_combobox.get()
    coin_id = coin_ids.get(ticker)
    price = get_price(coin_id)
    if price is not None:
        label.config(text=f'${price:.2f}')
    else:
        label.config(text='Ошибка загрузки')






def on_select(event):
    selected_item = kripto_combobox.get()
    label.config(text=selected_item, width=50)



def update_label(event=None):
    ticker = kripto_combobox.get()
    coin_id = coin_ids.get(ticker)
    price = get_price(coin_id)
    if price is not None:
        label.config(text=f'${price:.2f}')
    else:
        label.config(text='Ошибка')

def get_price(coin_id):
    url = f'{base_url}/simple/price'
    params = {
        'ids' : coin_id,
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get(coin_id, {}).get('usd')
    except requests.exceptions.HTTPError as e:
        print(f'Ошибка HTTP: {e}')
        return None
    except (KeyError, ValueError) as e:
        print(f'Ошибка данных: {e}')
        return None

kriptovaluta = {
    'BTC' : 'Bitcoin',
    'ETH' : 'Ethereum',
    'USDT' : 'Tether',
    'BNB' : 'Binance Coin',
    'XRP' : 'Ripple',
    'USDC' : 'USD Coin',
    'SOL' : 'Solana'
}

coin_ids = {
    'BTC' : 'bitcoin',
    'ETH' : 'ethereum',
    'USDT' : 'tether',
    'BNB' : 'binancecoin',
    'XRP' : 'ripple',
    'USDC' : 'usd-coin',
    'SOL' : 'solana'
}


window = Tk()
window.title('Текущие курсы криптовалют')
window.geometry('338x330')

Label(text='Популярные криптовалюты', font=('Helvetica', 10), relief='solid', borderwidth=2,  anchor='center', bg='white').pack(pady=10)


kripto_combobox = ttk.Combobox(window, values= list(kriptovaluta.keys()), state='readonly')
kripto_combobox.current(0)
kripto_combobox.bind('<<ComboboxSelected>>', update_label)
kripto_combobox.pack()
label = Label(font=('Arial', 14))
label.pack()

# Button(text='Получить курс обмена криптовалют к доллару',
#        command=exchange).pack(pady=10, padx=10)






window.mainloop()