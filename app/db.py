import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn

def init_db():
    """Создаёт таблицу tasks, если она не существует."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_all_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description FROM tasks ORDER BY id;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': t[0], 'title': t[1], 'description': t[2]} for t in tasks]

def create_task(title, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id;",
        (title, description)
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return task_id

def get_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description FROM tasks WHERE id = %s;", (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()
    if task:
        return {'id': task[0], 'title': task[1], 'description': task[2]}
    return None

def update_task(task_id, title, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET title = %s, description = %s WHERE id = %s;",
        (title, description, task_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
