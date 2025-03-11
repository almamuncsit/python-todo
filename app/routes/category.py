from flask import Blueprint, request, jsonify
from app import db
from app.models import Category

bp = Blueprint('category', __name__)

@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'created_at': category.created_at
    } for category in categories])

@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
        
    category = Category(name=data['name'])
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Category name already exists'}), 400

@bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
        
    try:
        category.name = data['name']
        db.session.commit()
        return jsonify({
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Category name already exists'}), 400

@bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Cannot delete category with existing tasks'}), 400