import json
import openai

key = ""

def process_req_initial(events: list, ages: list, gender: str):
    client = openai.OpenAI(
      api_key=key
    )
    age_event_dictionary = dict(zip(ages, events))
    # Convert age_event_dictionary to a JSON string
    age_event_json = json.dumps(age_event_dictionary)

    # Construct initial prompt using events, ages, gender, and dictionary
    initial_prompt = f"The {gender} at these ages did the corresponding events as follows:\n"
    initial_prompt += f"Age-event dictionary: {age_event_json}\n"
    initial_prompt += f"Based on this information, what are 3 questions you would ask this {gender}s future self about their past to get to know their personality before age {ages[-1]} better ? Limit the questions to not be too long. Do not ask question that refer to a specific age number. Make the JSON key that has the list of 3 questions always be 'questions'"
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    response_format={"type": "json_object"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": initial_prompt}
      ]
    )
    q_dict = json.loads(response.choices[0].message.content)
    print(q_dict)
    return q_dict['questions']

def process_req_fin(age_events, questions_dict, gender):
    client = openai.OpenAI(
        api_key=key
    )
    # Combine events and questions into a single prompt
    prompt = ""
    prompt += "These are the life events of a " + gender + ":\n"
    for age, event in age_events.items():
        prompt += f"Age: {age}\nLife Event: {event}\n\n"
    prompt += "And these are some questions answered by this " + gender + ":\n"
    for question, answer in questions_dict.items():
        prompt += f"Question: {question}\nAnswer: {answer}\n\n"
    prompt += "Based on this information, give an alternate future for this person for the next 10 years starting from " + str(min(age_events)) + ". Give 5 age timestamps and" \
              "a description for each timestamp on what they are doing."
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt + "Make the JSON key that has the response be 'prediction' and make the value a dictionary"
                                                 " of length 5 for each age timestamp and event description pair, where the key is the age as an integer"}
        ]
    )

    text_predictions_dict = json.loads(response.choices[0].message.content)
    text_predictions = list(text_predictions_dict['prediction'].values())
    text_predict_ages = list(text_predictions_dict['prediction'].keys())
    text_predict_ages.sort()
    url_list = []
    # for i in range(5):
    #     response2 = client.images.generate(
    #         model="dall-e-2",
    #         prompt="A " + gender + " who is persian and aged " + str(text_predict_ages[i]) + " during the 21st century in the following event:" + text_predictions[i],
    #         size="512x512",
    #         quality="standard",
    #         n=1,
    #     )
    #     print("done")
    #     url_list.append(response2.data[0].url)

    return (text_predictions, text_predict_ages, url_list)
