
from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = 'items.json'

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(load_items())

@app.route('/items', methods=['POST'])
def add_item():
    items = load_items()
    new_item = request.get_json()
    items.append(new_item)
    save_items(items)
    return jsonify({'status': 'added'}), 201
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    items = load_items()
    updated_data = request.get_json()
    for item in items:
        if item['id'] == item_id:
            item.update(updated_data)
            save_items(items)
            return jsonify({'status': 'updated'})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)