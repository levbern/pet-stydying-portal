import sqlite3

# Подключение к Базе данных
conn = sqlite3.connect("static/data/site.db")

# Курсор
cursor = conn.cursor()

name = '🚀 Первые шаги'
text = 'Заверши первый урок в любом курсе'
type = 'first_lesson'
# SQL-запрос
cursor.execute("""
            INSERT INTO achievements (name, text, type)
            VALUES (?, ?, ?)
        """, (name, text, type))

conn.commit()

conn.close()