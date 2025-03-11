import pytest
from app.models import Task, Category
from app import db

@pytest.fixture
def category(client):
    response = client.post('/categories', json={'name': 'Work'})
    return response.json

def test_create_task(client, category):
    task_data = {
        'title': 'Complete Project',
        'description': 'Finish the todo app',
        'category_id': category['id'],
        'priority': 'high',
        'due_date': '2024-01-20T10:00:00Z'
    }
    
    response = client.post('/tasks', json=task_data)
    assert response.status_code == 201
    assert response.json['title'] == task_data['title']
    assert response.json['category_id'] == category['id']

def test_get_tasks(client, category):
    # Create test tasks
    task_data = {
        'title': 'Task 1',
        'category_id': category['id']
    }
    client.post('/tasks', json=task_data)
    
    task_data['title'] = 'Task 2'
    client.post('/tasks', json=task_data)
    
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['title'] == 'Task 1'
    assert response.json[1]['title'] == 'Task 2'

def test_update_task(client, category):
    # Create a task first
    task_data = {
        'title': 'Original Task',
        'category_id': category['id']
    }
    response = client.post('/tasks', json=task_data)
    task_id = response.json['id']
    
    # Update the task
    update_data = {
        'title': 'Updated Task',
        'status': True
    }
    response = client.put(f'/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['title'] == update_data['title']
    assert response.json['status'] == update_data['status']

def test_delete_task(client, category):
    # Create a task first
    task_data = {
        'title': 'Test Task',
        'category_id': category['id']
    }
    response = client.post('/tasks', json=task_data)
    task_id = response.json['id']
    
    # Delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    
    # Verify task is deleted
    response = client.get('/tasks')
    assert len(response.json) == 0