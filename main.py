import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# Настройка API
API_KEY = 'ВАШ_API_КЛЮЧ'
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

# Загрузка истории
history = []
if os.path.exists('history.json'):
    with open('history.json', 'r') as f:
        history = json.load(f)

# Функции
def save_history():
    with open('history.json', 'w') as f:
        json.dump(history, f)

def update_history():
    listbox_history.delete(0, tk.END)
    for item in reversed(history[-20:]):
        listbox_history.insert(tk.END, item)

def get_rates():
    response = requests.get(API_URL)
    data = response.json()
    return data['conversion_rates']

def convert():
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительное число")
        return
    from_curr = combo_from.get()
    to_curr = combo_to.get()

    try:
        rates = get_rates()
        rate = rates[to_curr]
        result = amount * rate
        result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}")
        # История
        operation = f"{amount} {from_curr} -> {result:.2f} {to_curr}"
        history.append(operation)
        update_history()
        save_history()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить курс: {e}")

# GUI
root = tk.Tk()
root.title("Currency Converter")

# Поле ввода
tk.Label(root, text="Сумма").grid(row=0, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1)

# Выбор валют
currencies = ['USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CNY']
ttk.Label(root, text="Из").grid(row=1, column=0)
combo_from = ttk.Combobox(root, values=currencies, state='readonly')
combo_from.current(0)
combo_from.grid(row=1, column=1)

ttk.Label(root, text="В").grid(row=2, column=0)
combo_to = ttk.Combobox(root, values=currencies, state='readonly')
combo_to.current(1)
combo_to.grid(row=2, column=1)

# Конвертировать
btn_convert = tk.Button(root, text="Конвертировать", command=convert)
btn_convert.grid(row=3, column=0, columnspan=2, pady=5)

# Результат
result_label = tk.Label(root, text="Результат появится здесь")
result_label.grid(row=4, column=0, columnspan=2)

# История
tk.Label(root, text="История операций").grid(row=5, column=0, columnspan=2)
listbox_history = tk.Listbox(root, height=10, width=50)
listbox_history.grid(row=6, column=0, columnspan=2)
update_history()

root.mainloop()
