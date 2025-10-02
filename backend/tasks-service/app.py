from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Mock database
tasks = []
task_id_counter = 1

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Tasks service is running',
        'timestamp': datetime.now().isoformat(),
        'total_tasks': len(tasks)
    })

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    })

# Create new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify({'message': 'Task created successfully', 'task': task}), 201

# Get task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'task': task})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)