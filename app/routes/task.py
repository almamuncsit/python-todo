from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Task, Category

bp = Blueprint('task', __name__)

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'status': task.status,
        'category_id': task.category_id,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    } for task in tasks])

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    
    if not data or not all(k in data for k in ('title', 'category_id')):
        return jsonify({'error': 'Title and category_id are required'}), 400
    
    # Verify category exists
    category = Category.query.get_or_404(data['category_id'])
    
    # Convert due_date string to datetime if provided
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        due_date=due_date,
        priority=data.get('priority', 'medium'),
        category_id=data['category_id']
    )
    
    try:
        db.session.add(task)
        db.session.commit()
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'priority': task.priority,
            'status': task.status,
            'category_id': task.category_id,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'due_date' in data:
        try:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']
    if 'category_id' in data:
        Category.query.get_or_404(data['category_id'])
        task.category_id = data['category_id']
    
    try:
        db.session.commit()
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'priority': task.priority,
            'status': task.status,
            'category_id': task.category_id,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400