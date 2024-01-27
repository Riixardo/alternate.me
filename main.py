import openai

def process_req_initial():
    client = openai.OpenAI(
      api_key="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"
    )
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      response_format={"type": "json_object"},
      messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "The boy at age 5 was a very hard worker. At age 10 he persisted his hard working nature and "
                                    "delivered newspapers in the Boston area. And now in the present, when he is 12, his parents divorced and he went into a state of loneliness. Based on this information"
                                    "what are 3 questions you may need to ask the boy to predict his future past age 12 for another 10 years? Format the questions in past-tense, as if you are asking the future version of that boy."}
      ]
    )

    print(response.choices[0].message.content + "\n")

    return response.choices[0].message.content
