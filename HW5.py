
from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = 'data/items.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data), 200


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    for item in data:
        if item['id'] == item_id:
            return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404


@app.route('/items', methods=['POST'])
def create_item():
    data = load_data()
    new_item = request.get_json()
    new_item['id'] = max([item['id'] for item in data], default=0) + 1
    data.append(new_item)
    save_data(data)
    return jsonify(new_item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    updated_item = request.get_json()
    for i, item in enumerate(data):
        if item['id'] == item_id:
            updated_item['id'] = item_id
            data[i] = updated_item
            save_data(data)
            return jsonify(updated_item), 200
    return jsonify({'error': 'Item not found'}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    for i, item in enumerate(data):
        if item['id'] == item_id:
            data.pop(i)
            save_data(data)
            return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    app.run(debug=True)
