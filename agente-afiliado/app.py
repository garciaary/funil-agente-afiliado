from flask import Flask, render\_template, request 

app = Flask(**name**) 

@app.route('/')  
def index():  
return render\_template('index.html') 

@app.route('/quiz')  
def quiz():  
return render\_template('quiz.html') 

@app.route('/resultado')  
def resultado():  
categoria = request.args.get('categoria', '')  
perfil = request.args.get('perfil', '')  
return render\_template('resultado.html', categoria=categoria, perfil=perfil) 

if **name** == '**main**':  
app.run(debug=True)