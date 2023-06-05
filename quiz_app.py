from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Define the quiz questions and answers
questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['Paris', 'London', 'Berlin', 'Rome'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'choices': ['Mars', 'Venus', 'Jupiter', 'Mercury'],
        'correct_answer': 'Mars'
    },
    {
        'question': 'What is the largest ocean in the world?',
        'choices': ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
        'correct_answer': 'Pacific Ocean'
    }
]

score = 0
current_question = 0
message = ""

@app.route('/', methods=['GET', 'POST'])
def quiz():
    global score
    global current_question
    global message

    if request.method == 'POST':
        user_answer = request.form.get('choice')

        if user_answer:
            if user_answer == questions[current_question]['correct_answer']:
                message = "Correct"
                score += 10
            else:
                message = "Incorrect"


            current_question += 1

            if current_question >= len(questions):
                return redirect('/result')
        else:
            message = "Please select an answer."

            return render_template('quiz.html', question=questions[current_question], score=score, current_question=current_question, message=message)

    return render_template('quiz.html', question=questions[current_question], score=score, current_question=current_question, message=message)

@app.route('/result')
def result():
    global score
    score_message = f"Your score: {score}"
    score = 0
    current_question = 0
    return render_template('result.html', message=score_message)


if __name__ == '__main__':
    app.run(debug=True)

