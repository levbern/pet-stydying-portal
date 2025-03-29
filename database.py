import sqlite3

def get_user(user_id):
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    user_data = cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user_data

def get_user_achievements(user_id):
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    ach_list = cursor.execute("""SELECT name, text FROM achievements WHERE achievement_id IN (SELECT achievement_id FROM achievementsUsers WHERE user_id = ?)""", (user_id,)).fetchall()
    conn.close()
    return ach_list
    

def login_user(username):
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password_hash FROM users WHERE login = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def add_user_achiev(user_id, type):
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    achievement_id = cursor.execute("SELECT achievement_id FROM achievements WHERE type = ?", (type,)).fetchone()[0]
    query = f"""INSERT INTO achievementsUsers(achievement_id, user_id) VALUES (?, ?)"""
    cursor.execute(query, (achievement_id, user_id,))
    conn.commit()
    conn.close()

def add_user(data):
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (name, surname, patronymic, login, email, password_hash) VALUES (?, ?, ?, ?, ?, ?)""", (
        data['name'], data['surname'], data['patronymic'],
        data['username'], data['email'], data['password']
    ))
    conn.commit()
    conn.close()

def add_course(data, user_id):
    print(data)
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO courses (user_id, name, description) VALUES (?, ?, ?)""", (user_id, data['course_name'], data['description']))
    conn.commit()
    course_id = cursor.execute("""SELECT course_id FROM Courses WHERE creator_id = ? AND name = ?""", (user_id, data['course_name']))
    cursor.execute("""INSERT INTO userCourse (user_id, course_id, role) VALUES (?, ?, ?)""", (user_id, course_id, 1))
    conn.commit()
    #cursor.
    conn.close()