from flask import Flask, render_template, request, jsonify
from main import process_req_initial, process_req_fin

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/loading.html')
def loading():
    return render_template('loading.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/timeline.html')
def timeline():
    return render_template('timeline.html')

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
    gender = data['gender']
    eth = data['eth']
    age_event = {}
    ages_list = eval(data['ages'])
    for i in range(len(ages_list)):
        age_event[ages_list[i]] = data['events'][i]

    # Process the answers and predict the future
    prediction = process_req_fin(age_event, questions_answers_dictionary, gender, eth)

    return jsonify({'prediction': prediction[0], 'ages': prediction[1], 'image': prediction[2]})

if __name__ == '__main__':
    app.run(debug=True)
