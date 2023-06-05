from flask import Flask, render_template, request, redirect

import os
import openai
import json


openai.api_key  = "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" 

app = Flask(__name__)
app.session.permanent = True

score = 0
current_question = 0
message = ""

delimiter = "####"
system_message = f"""
You are a quiz for capitals of the world. \
Generate question, 4 possible choices, correct answer. \
The output should only be in JSON format. \
Use following keys "question", "choices", "correct_answer", "difficulty", "country". 
The countries between delimiter {delimiter} are already asked. 
Do not repeat these countries \

"""
difficulty = "easy"
#messages = [{"role": "system", "content": system_message},
#            {"role": "assistant", "content": "Generate an " + difficulty + " question for the above system"},
#           ]
questions = {}
correct_answer = ""

@app.route('/', methods=['GET', 'POST'])
def quiz():
    global score
    global current_question
    global message
    global delimiter
    global system_message
    global difficulty
    global messages
    global correct_answer
    global questions
    if request.method == 'GET':
        questions = get_question()
        correct_answer = questions["correct_answer"]
    if request.method == 'POST':
        user_answer = request.form.get('choice')
        if user_answer:
            if user_answer == correct_answer:
                score += 10
                increase_difficulty()
                print(score)

            else: 
                decrease_difficulty()
            current_question += 1

            #if request.form['action'] == 'END':
                #return redirect('/result')
        else:
            message = "Please select an answer."
        questions = get_question()
        correct_answer = questions["correct_answer"]

        return render_template('quiz.html', question=questions, score=score, current_question=current_question, message=message)

    return render_template('quiz.html', question=questions, score=score, current_question=current_question, message=message)

@app.route('/result', methods=['POST'])
def result():
    global score
    score_message = f"Your score: {score}"
    #score = 0
    #current_question = 0
    return render_template('result.html', message=score_message)

def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
        presence_penalty=2
    )
    return response.choices[0].message["content"]

def get_question():
    global delimiter
    global system_message
    global difficulty
    #print(messages)
    messages = [{"role": "system", "content": system_message},
            {"role": "assistant", "content": "Generate an " + difficulty + " question for the above system"},
           ]
    response = get_completion_from_messages(messages)
    data = json.loads(response)
    questions = {}
    questions["question"], questions["choices"],questions["correct_answer"], country = data["question"], data["choices"], data["correct_answer"], data["country"]
    #print(data["country"])
    #print(response)
    system_message = f"{system_message} {delimiter} {country} {delimiter} \n"
    #print(system_message)    
    return questions

def increase_difficulty():
    global difficulty
    if difficulty == "easy":
        difficulty = "medium"
    if difficulty == "medium":
        difficulty = "hard"

def decrease_difficulty():
    global difficulty
    if difficulty == "hard":
        difficulty = "medium"
    if difficulty == "medium":
        difficulty = "easy"

if __name__ == '__main__':
    app.run(debug=False)

