from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DATABASE = 'database.db'

# ============================================
# SEUS LINKS DE AFILIADO — TROQUE AQUI
# ============================================
AFFILIATE_LINKS = {
     'A': 'https://go.hotmart.com/S106430936D?ap=1c6a',
    'B': 'https://go.hotmart.com/S106430936D?ap=1c6a',
    'C': 'https://go.hotmart.com/S106430936D?ap=1c6a'


}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                profile_result TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

from quiz_flow import quiz_questions, profiles

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'quiz_progress' not in session:
        session['quiz_progress'] = 0
        session['profile_weights'] = {'A': 0, 'B': 0, 'C': 0}

    if request.method == 'POST':
        selected_option_index = int(request.form['answer'])
        current_question_index = session['quiz_progress']
        selected_option = quiz_questions[current_question_index]['options'][selected_option_index]

        for profile_key, weight in selected_option['weight'].items():
            session['profile_weights'][profile_key] += weight

        session['quiz_progress'] += 1

        if session['quiz_progress'] >= len(quiz_questions):
            max_weight = -1
            result_profile_key = None
            for key, weight in session['profile_weights'].items():
                if weight > max_weight:
                    max_weight = weight
                    result_profile_key = key
                elif weight == max_weight and result_profile_key is not None:
                    if key == 'A' and result_profile_key != 'A':
                        result_profile_key = 'A'
                    elif key == 'B' and result_profile_key == 'C':
                        result_profile_key = 'B'
            session['result_profile_key'] = result_profile_key
            return redirect(url_for('resultado'))
        else:
            return redirect(url_for('quiz'))

    current_question_index = session['quiz_progress']
    question = quiz_questions[current_question_index]
    return render_template('quiz.html', question=question, question_num=current_question_index + 1, total_questions=len(quiz_questions))

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
    if 'result_profile_key' not in session:
        return redirect(url_for('index'))

    profile_key = session['result_profile_key']
    profile = profiles[profile_key]

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        profile_result = request.form['profile_result']

        # Salva o lead no banco
        conn = get_db_connection()
        conn.execute('INSERT INTO leads (name, email, profile_result) VALUES (?, ?, ?)',
                     (name, email, profile_result))
        conn.commit()
        conn.close()

        # Redireciona para o link de afiliado do perfil
        affiliate_url = AFFILIATE_LINKS.get(profile_key, 'https://google.com')
        return redirect(affiliate_url)

    return render_template('resultado.html', profile=profile, profile_key=profile_key, offer_submitted=False)

if __name__ == '__main__':
    app.run(debug=True)