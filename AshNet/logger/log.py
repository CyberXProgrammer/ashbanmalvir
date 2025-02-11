from flask import Flask, send_from_directory, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = 'https://discord.com/api/webhooks/1277983479887433759/eaiB2nhKDP9hT284iVD7wC8_qHMxEff4vtdjtn4QaIu9AnmQV3fxy5GvWqVYXdTjUXGp'

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/log_click', methods=['POST'])
def log_click():
    payload = {'content': 'Someone clicked the image!'}
    requests.post(WEBHOOK_URL, json=payload)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
