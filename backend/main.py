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
    initial_prompt += f"Based on this information, what are 3 questions you may need to ask the {gender} to predict his future past age {ages[-1]} for another 10 years? Format the questions in past-tense. Limit the questions to not be too long. Do not ask question that refer to a specific age number. Make the JSON key that has the list of 3 questions always be 'questions'"
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": initial_prompt}
      ]
    )
    q_dict = json.loads(response.choices[0].message.content)
    print(q_dict)
    return q_dict['questions']

def process_req_fin(events, questions_dict):
    client = openai.OpenAI(
        api_key=key
    )
    # Combine events and questions into a single prompt
    prompt = "I gave you the list of Events initially to ask some quesitons from the user, and you genereate these questions. Now, I got the answers from the user for the questions. Write a short story about this person's current state using that list of events and the information you have from the user"
    prompt += "Events:\n" + "\n".join(events) + "\n\n"
    prompt += "Questions and Answers:\n"
    for question, answer in questions_dict.items():
        prompt += f"Question: {question}\nAnswer: {answer}\n\n"

        # Send the prompt to OpenAI for completion



    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt + "Make the JSON key that has the respnose be 'prediction'"}
        ]
    )

    return response.choices[0].message.content
