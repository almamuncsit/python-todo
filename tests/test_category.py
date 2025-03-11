import pytest
from app.models import Category
from app import db

def test_create_category(client):
    response = client.post('/categories', json={'name': 'Work'})
    assert response.status_code == 201
    assert response.json['name'] == 'Work'

def test_get_categories(client):
    # Create test categories
    client.post('/categories', json={'name': 'Work'})
    client.post('/categories', json={'name': 'Personal'})
    
    response = client.get('/categories')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'Work'
    assert response.json[1]['name'] == 'Personal'

def test_update_category(client):
    # Create a category first
    response = client.post('/categories', json={'name': 'Work'})
    category_id = response.json['id']
    
    # Update the category
    response = client.put(f'/categories/{category_id}', json={'name': 'Job'})
    assert response.status_code == 200
    assert response.json['name'] == 'Job'

def test_delete_category(client):
    # Create a category first
    response = client.post('/categories', json={'name': 'Work'})
    category_id = response.json['id']
    
    # Delete the category
    response = client.delete(f'/categories/{category_id}')
    assert response.status_code == 200
    
    # Verify category is deleted
    response = client.get('/categories')
    assert len(response.json) == 0