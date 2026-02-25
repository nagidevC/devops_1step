from flask import Flask, request, jsonify, send_from_directory
import os
from app.db import init_db, get_all_tasks, create_task, get_task, update_task, delete_task

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Инициализация БД при старте
init_db()

# Главная страница - отдаём наш фронтенд
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# API: получить все задачи
@app.route('/api/tasks', methods=['GET'])
def tasks_get():
    tasks = get_all_tasks()
    return jsonify(tasks)

# API: создать задачу
@app.route('/api/tasks', methods=['POST'])
def tasks_post():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    task_id = create_task(title, description)
    return jsonify({'id': task_id}), 201

# API: получить одну задачу
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def task_get(task_id):
    task = get_task(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

# API: обновить задачу
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def task_put(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    update_task(task_id, title, description)
    return jsonify({'success': True})

# API: удалить задачу
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def task_delete(task_id):
    delete_task(task_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
