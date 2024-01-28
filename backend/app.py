from flask import Flask, jsonify, request
from main import process_req_fin, process_req_initial

app = Flask(__name__)

# New route to handle button click and receive data from the front end
@app.route('/send_init_data', methods=['POST'])
def send_init_data():
    data = request.get_json()
    questions = process_req_initial(data['events'], data['age_arr'], data['gender'])
    result = f"Received data: {data['gender']}"
    return jsonify({'result': result, 'questions': questions})


@app.route('/send_fin_data', methods=['POST'])
def send_fin_data():
    data = request.get_json()
    questions_answers_dictionary = dict(zip(data['questions'],data['answers']))
    events = data['events']

    # Process the answers and predict the future
    prediction = process_req_fin(events, questions_answers_dictionary)

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    # Change the host and port as needed
    app.run(host='localhost', port=5000, debug=True)
