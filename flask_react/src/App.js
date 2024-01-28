import React, { useState } from 'react';

const App = () => {
  const [response, setResponse] = useState('');
  const [prediction, setPrediction] = useState('');

  const sendInitRequest = async () => {
    const events = [
      'The boy at age 5 was a very hard worker.',
      'At age 10 he persisted his hard working nature and delivered newspapers in the Boston area. And now in the present, when he is 12, his parents divorced and he went into a state of loneliness.'
    ];

    try {
      const response = await fetch('/send_init_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ gender: 'male', events: events, age_arr: [5, 10, 12] })
      });

      const data = await response.json();
      sessionStorage.setItem('questions', JSON.stringify(data.questions));
      sessionStorage.setItem('events', JSON.stringify(events));

      setResponse('Backend Response: ' + data.result + ' + ' + data.questions[0]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const sendFinRequest = async () => {
    try {
      const questions = JSON.parse(sessionStorage.getItem('questions'));
      const events = JSON.parse(sessionStorage.getItem('events'));

      // Check if questions and events are null
      if (!questions || !events) {
        console.error('Questions or events are null.');
        return;
      }

      const answers = [];
      questions.forEach((question) => {
        const answer = prompt(question);
        answers.push(answer);
      });

      const response = await fetch('/send_fin_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ questions: questions, answers: answers, events: events })
      });

      const data = await response.json();
      setPrediction('Future: ' + data.prediction);

      // Handle the prediction result
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <button onClick={sendInitRequest}>Send Init Data to Backend</button>
      <button onClick={sendFinRequest}>Send Final Data to Backend</button>
      <p id="response">{response}</p>
      <p id="prediction">{prediction}</p>
      <p>Hello!!!!</p>
    </div>
  );
};

export default App;
