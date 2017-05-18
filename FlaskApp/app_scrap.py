from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz_answers', methods=['POST'])
def quiz_answers():
    q1 = request.form['q1']
    q2 = request.form['q2']
    q4 = request.form['q4']
    q5 = request.form['q5']

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')