@app.route('/resultado')
def resultado():
    categoria = request.args.get('categoria', '')
    perfil = request.args.get('perfil', '')
    return render_template('resultado.html', categoria=categoria, perfil=perfil)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/')
def index():
    return render_template('index.html')