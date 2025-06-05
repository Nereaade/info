import json, os
from flask import Blueprint, jsonify, request, render_template

items_bp = Blueprint('items', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/items.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@items_bp.route('/')
def index():
    return render_template('index.html')

@items_bp.route('/items', methods=['GET'])
def get_items():
    return jsonify(load_data()), 200

@items_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = load_data()
    item = next((i for i in items if i['id'] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

@items_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if 'id' not in data or 'name' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    items = load_data()
    items.append(data)
    save_data(items)
    return jsonify(data), 201

@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    new_data = request.get_json()
    items = load_data()
    for i, item in enumerate(items):
        if item['id'] == item_id:
            items[i].update(new_data)
            save_data(items)
            return jsonify(items[i]), 200
    return jsonify({'error': 'Item not found'}), 404

@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()
    new_items = [i for i in items if i['id'] != item_id]
    if len(new_items) == len(items):
        return jsonify({'error': 'Item not found'}), 404
    save_data(new_items)
    return jsonify({'message': 'Item deleted'}), 200
