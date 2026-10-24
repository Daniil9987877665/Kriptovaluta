import tkinter # Главный модуль библиотеки для создания графического интерфейса
from tkinter import *  # Импорт всех публичных имён tkinter (Tk, Label и т.д.) без префикса
from tkinter import messagebox as mb # Модуль диалоговых окон (сообщения, предупреждения) под псевдонимом mb
from tkinter import ttk # Модуль "тематических" виджетов (Combobox, Progressbar и др.)
import requests # Библиотека для отправки HTTP-запросов к API
import json # Модуль для работы с JSON

def exchange():
    """Настройки для обращения к CoinGecko API"""
    base_url = 'https://api.coingecko.com/api/v3' # Базовый адрес CoinGecko API (версия v3)
    api = 'CG-LGbLjNCxJ7qcSKsR6tjaZAvr'    # персональный Demo-ключ API

    headers = {                     # Словарь HTTP-заголовков, отправляемых с запросом
        'accept': 'application/json',  # Клиент ожидает ответ в формате JSON
        'x-cg-demo-api-key': api   # Заголовок с ключом доступа к Demo-тарифу
    }

    url = f'{base_url}/simple/price'  # Итоговый адрес эндпоинта, возвращающего текущие цены
    params = {                        # Query-параметры запроса
        'ids': 'bitcoin,solana',      # ID монет через запятую (API-ID, не тикеры)
        'vs_currencies': 'usd'        # Валюта, в которой вернуть цену (доллары США)
    }

    """Запрос к API и вывод результата в консоль"""
    try:                              # Начало блока обработки исключений — защита от падения программы
        response = requests.get(url, params=params, headers=headers, timeout=10)
        # Отправляем GET-запрос:
        # url      — адрес эндпоинта
        # params   — параметры (requests сам добавит ?ids=...&vs_currencies=...)
        # headers  — заголовки с ключом API
        # timeout  — максимум 10 секунд ожидания ответа
        response.raise_for_status()
        # Если сервер вернул HTTP-ошибку (4xx или 5xx), выбрасывает исключение HTTPError

        data = response.json()
        # Парсит тело ответа из JSON в Python-словарь:
        # {'bitcoin': {'usd': 67000.5}, 'solana': {'usd': 150.2}}
        # print('Данные успешно получены')        # Информационное сообщение в консоль
        # print(f"Bitcoin: ${data['bitcoin']['usd']:.2f}")
        # print(f"Solana: ${data['solana']['usd']:.2f}")

    except requests.exceptions.HTTPError as e:
        print(f'Ошибка HTTP: {e}')


def update_label(event):
    select_text = kripto_combobox.get()
    label.config(text=select_text)


def on_select(event):
    selected_item = kripto_combobox.get()

    res_entry.delete(0, END)
    res_entry.insert(0, f'Вы выбрали: {selected_item}')


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


kripto_combobox = ttk.Combobox(window, values= list(kriptovaluta.keys()), state='readonly')
kripto_combobox.current(0)
kripto_combobox.bind('<<ComboboxSelected>>', on_select)
kripto_combobox.pack()
res_entry = ttk.Entry(window, width=25)
res_entry.pack(pady=10)

Button(text='Получить курс обмена криптовалют к доллару',
       command=exchange).pack(pady=10, padx=10)






window.mainloop()