import sqlite3

# Подключение к Базе данных
conn = sqlite3.connect("static/data/site.db")

# Курсор
cursor = conn.cursor()
# SQL-запрос
cursor.execute("""INSERT INTO TaskCourse (number, task_id, course_id, type)
SELECT 
    MAX(number) + 1,
    test_id,
    1,
    'test'
FROM TaskCourse 
CROSS JOIN Test
WHERE name IN ('Промежуточный тест', 'Финальный экзамен');""")

conn.commit()

conn.close()