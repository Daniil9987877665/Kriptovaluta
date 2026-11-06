import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


# ==================== КОНСТАНТЫ ====================

base_url = 'https://api.coingecko.com/api/v3'
api_key = 'CG-LGbLjNCxJ7qcSKsR6tjaZAvr'
headers = {
    'accept': 'application/json',
    'x-cg-demo-api-key': api_key
}

coin_ids = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'binancecoin': 'BNB',
    'solana': 'SOL',
    'ripple': 'XRP'
}

currencies = ['usd', 'eur', 'rub']
refresh_interval = 60


# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================

current_data = {}
current_currency = 'usd'


# ==================== ФУНКЦИИ ====================

def get_prices():
    """Запрашивает у API цены всех монет сразу во всех валютах.
    Возвращает словарь или None при ошибке."""
    url = f'{base_url}/simple/price'
    params = {
        'ids': ','.join(coin_ids.keys()),
        'vs_currencies': ','.join(currencies)
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка сети: {e}')
        return None


def fetch_and_update():
    """Получает данные и обновляет интерфейс.
    Выполняется в главном потоке (без threading и queue)."""
    global current_data

    status_label.config(text='Загрузка...', fg='orange')
    window.update()   # Принудительно перерисовать окно перед запросом

    data = get_prices()

    if data is None:
        status_label.config(text='Ошибка загрузки', fg='red')
        messagebox.showerror('Ошибка', 'Не удалось получить данные от API.\nПроверьте интернет-соединение.')
        return

    current_data = data
    time_label.config(text=datetime.now().strftime('%H:%M:%S'))
    status_label.config(text='Данные обновлены', fg='green')
    render_table()


def render_table():
    """Перерисовывает таблицу с ценами в выбранной валюте."""
    for row in tree.get_children():
        tree.delete(row)

    for coin_id, ticker in coin_ids.items():
        price = current_data.get(coin_id, {}).get(current_currency)
        if price is not None:
            price_str = f'{price:,.2f} {current_currency.upper()}'
        else:
            price_str = '—'
        tree.insert('', 'end', values=(ticker, price_str))


def on_currency_change(event=None):
    """Срабатывает при выборе другой валюты."""
    global current_currency
    current_currency = currency_combobox.get().lower()
    render_table()


def schedule_auto_refresh():
    """Планирует автообновление каждые refresh_interval секунд."""
    fetch_and_update()
    window.after(refresh_interval * 1000, schedule_auto_refresh)


# ==================== ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ====================

window = tk.Tk()
window.title('CriptoMonitor ')
window.geometry('600x450')
window.iconbitmap('favicon.ico')

# --- Верхняя панель: выбор валюты, кнопка, время ---
top_frame = tk.Frame(window, padx=8, pady=8)
top_frame.pack(fill='x')

tk.Label(top_frame, text='Базовая валюта:').pack(side='left')

currency_combobox = ttk.Combobox(
    top_frame,
    values=[c.upper() for c in currencies],
    state='readonly',
    width=6
)
currency_combobox.set('USD')
currency_combobox.bind('<<ComboboxSelected>>', on_currency_change)
currency_combobox.pack(side='left', padx=6)

refresh_button = tk.Button(top_frame, text='Обновить', command=fetch_and_update)
refresh_button.pack(side='left', padx=6)

tk.Label(top_frame, text='Обновлено:').pack(side='left', padx=(20, 4))
time_label = tk.Label(top_frame, text='—')
time_label.pack(side='left')

# --- Таблица с ценами ---
columns = ('ticker', 'price')
tree = ttk.Treeview(window, columns=columns, show='headings')
tree.heading('ticker', text='Монета')
tree.heading('price', text='Цена')
tree.column('ticker', width=150, anchor='w')
tree.column('price', width=250, anchor='e')
tree.pack(fill='both', expand=True, padx=8, pady=8)

# --- Строка статуса внизу ---
status_label = tk.Label(window, text='Готово', fg='black', anchor='w', relief='sunken')
status_label.pack(fill='x', side='bottom')


# ==================== ЗАПУСК ====================

schedule_auto_refresh()
window.mainloop()