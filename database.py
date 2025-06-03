import sqlite3
from sqlite3 import IntegrityError

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
    
def get_courses():
    courses = []
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    data_courses = cursor.execute("""SELECT name, description, subject, tags, course_id FROM courses""").fetchall()
    conn.close()
    for dc in data_courses:
        course = dict()
        course['name'] = dc[0]
        course['description'] = dc[1]
        course['subject'] = dc[2]
        course['tags'] = dc[3].split(',')
        course['id'] = dc[4]
        courses.append(course)
    return courses

def get_course(course_id):
    course = dict()
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    dc = cursor.execute("""SELECT name, description, subject, tags, course_id, finished, creator_id FROM courses WHERE course_id = ?""", (course_id,)).fetchone()
    print(dc)
    conn.close()
    course['name'] = dc[0]
    course['description'] = dc[1]
    course['subject'] = dc[2]
    course['tags'] = dc[3].split(',')
    course['id'] = dc[4]
    course['finished'] = dc[5]
    course['creator_id'] = dc[6]
    return course

def get_tasks(course_id):
    tasks = []
    conn = sqlite3.connect("static/data/site.db")
    cursor = conn.cursor()
    data_course = cursor.execute("""
    SELECT 
    COALESCE(L.name, T.name) AS title,
    COALESCE(L.description, T.description) AS description,
    TC.type AS material_type, TC.number
    FROM TaskCourse TC
    LEFT JOIN Lections L ON TC.task_id = L.lection_id AND TC.type = 'lection'
    LEFT JOIN Test T ON TC.task_id = T.test_id AND TC.type = 'test'
    WHERE TC.course_id = ?
    ORDER BY TC.number ASC""", (course_id,)).fetchall()
    conn.close()
    print(data_course)
    for dc in data_course:
        c = dict()
        c['name'] = dc[0]
        c['description'] = dc[1]
        c['type'] = dc[2]
        c['id'] = dc[3]
        tasks.append(c)
    return tasks

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
    conn = None
    try:
        conn = sqlite3.connect("static/data/site.db")
        cursor = conn.cursor()
        conn.execute("BEGIN")
        cursor.execute("""
            INSERT INTO courses (creator_id, name, description, subject, tags) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, data['course_name'], data['description'], data['subject'], data['tags']))
    
        course_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO userCourse (user_id, course_id, role) 
            VALUES (?, ?, ?)
        """, (user_id, course_id, 1))
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def add_lecture(lecture_name, description, content, course_id):
    conn = sqlite3.connect("static/data/site.db")
    try:
        with conn:
            cursor = conn.cursor()
            
            # 1. Вставка лекции
            cursor.execute("""
                INSERT INTO Lections (name, description, text)
                VALUES (?, ?, ?)
            """, (lecture_name, description, content))
            lecture_id = cursor.lastrowid
            
            # 2. Атомарное определение порядкового номера
            cursor.execute("""
                SELECT COALESCE(MAX(number), 0) + 1 
                FROM TaskCourse 
                WHERE course_id = ? AND type = 'lection'
            """, (course_id,))
            new_number = cursor.fetchone()[0]
            
            # 3. Связывание с курсом
            cursor.execute("""
                INSERT INTO TaskCourse (number, task_id, course_id, type)
                VALUES (?, ?, ?, 'lection')
            """, (new_number, lecture_id, course_id))
            
            return {"success": True, "lecture_id": lecture_id}
            
    except IntegrityError as e:
        return {"success": False, "error": f"Database integrity error: {str(e)}"}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
    finally:
        conn.close()