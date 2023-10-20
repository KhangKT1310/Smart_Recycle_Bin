from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'media'), path)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()['data']
        print('Received data:', data)
        # Do something with the data, for example, return it in the response
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
