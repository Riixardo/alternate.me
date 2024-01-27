from flask import Flask, render_template, request, jsonify
from main import process_req_initial

app = Flask(__name__, template_folder='template')

# Existing route for the homepage
@app.route('/')
def index():
    return render_template('home.html')

# New route to handle button click and receive data from the front end
@app.route('/send_data', methods=['POST'])
def send_data():
    data_from_frontend = request.get_json()
    # Process the data (in this case, just echoing it)
    questions = process_req_initial()
    result = f"Received data: {data_from_frontend['key']}"
    return jsonify({'result': result, 'questions': questions})

if __name__ == '__main__':
    app.run(debug=True)
