from flask import Flask, request, jsonify
import json
import os
from uuid import uuid4

app = Flask(__name__)
MESSAGES_FILE = 'messages.json'

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_messages(messages):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/get_messages')
def get_messages():
    return jsonify(load_messages())

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    messages = load_messages()
    
    new_message = {
        'id': str(uuid4()),
        'class': 'own' if data['username'] == 'current_user' else 'alien',
        'text': data['text'],
        'username': data['username']
    }
    
    messages.append(new_message)
    save_messages(messages)
    return jsonify({'status': 'success'})

@app.route('/delete_message/<msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    messages = load_messages()
    filtered = [m for m in messages if m['id'] != msg_id]
    
    if len(filtered) == len(messages):
        return jsonify({'status': 'not found'}), 404
    
    save_messages(filtered)
    return jsonify({'status': 'deleted'})
