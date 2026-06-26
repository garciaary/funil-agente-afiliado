from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/resultado')
def resultado():
    categoria = request.args.get('categoria', '')
    perfil = request.args.get('perfil', '')
    return render_template('resultado.html', categoria=categoria, perfil=perfil)

if __name__ == '__main__':
    app.run(debug=True)
