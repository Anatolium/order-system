import tkinter as tk
from tkinter import ttk
import sqlite3


def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        order_details TEXT NOT NULL,
        status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()


# Создаём главное окно приложения
app = tk.Tk()
app.title("Система управления заказами")

# Надпись не нужно сохранять в переменную, сразу размещаем её на экране.
# Создаём виджет метки Label в родительском окне app с текстом "Имя клиента".
# Label используется для отображения текста или изображений.
# pack() – метод геометрического менеджера, который управляет расположением виджетов внутри родительского контейнера.
# Вызов этого метода заставляет метку появиться в окне приложения
tk.Label(app, text="Имя клиента").pack()

# Создаём виджет поля ввода Entry
customer_name_entry = tk.Entry(app)
# Располагаем виджет поля ввода в родительском окне
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()


def view_orders():
    # Проходим через все записи в виджете tree и удаляем их, чтобы очистить виджет перед тем, как добавить новые записи
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    # Полученные из запроса строки извлекаются с помощью метода fetchall()
    rows = cur.fetchall()
    # Проходим по каждой из полученных строк и вставляем их в виджет tree для отображения данных о заказах.
    # Применяется метод insert объекта tree, который добавляет каждую строку как новую запись в виджете tree.
    # Аргумент "" указывает на корневой элемент дерева, tk.END на то, что данные следует добавить в конец списка
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()
    # Очищаем поля ввода от начала до конца
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()


add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Создаём виджет `Treeview` с помощью библиотеки ttk, который является частью tkinter и предназначен для отображения
# иерархических данных, расположенных в виде таблицы или дерева. Виджет Treeview широко используется для отображения
# списка элементов в виде таблицы с сортируемыми столбцами или структурированных данных в виде раскрывающегося дерева
columns = ("id", "customer_name", "order_details", "status")
# show="headings" означает, что в Treeview будут отображаться лишь заголовки столбцов, но не стандартные колонки дерева
# Это делает виджет похожим на обычную таблицу, где каждый столбец соответствует определенному полю данных
tree = ttk.Treeview(app, columns=columns, show="headings")

for column in columns:
    tree.heading(column, text=column)
tree.pack()

init_db()
view_orders()
app.mainloop()
