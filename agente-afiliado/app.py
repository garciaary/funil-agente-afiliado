import os  
from flask import Flask, render\_template, request, redirect, url\_for, session 

base\_dir = os.path.abspath(os.path.dirname(**file**))  
template\_dir = os.path.join(base\_dir, 'templates') 

app = Flask(**name**, template\_folder=template\_dir)  
app.secret\_key = 'chave\_secreta\_para\_sessoes\_seguras' 

QUIZZES = {  
'renda\_extra': \[  
{  
'id': 1,  
'texto': 'Quanto tempo por dia você tem livre para começar a faturar na internet?',  
'opcoes': {  
'A': 'Menos de 1 hora (quero algo rápido)',  
'B': 'De 1 a 3 horas (consigo me dedicar)',  
'C': 'Mais de 3 horas (quero focar 100%)'  
}  
},  
{  
'id': 2,  
'texto': 'Qual é o seu maior objetivo trabalhando como Agente de Vendas?',  
'opcoes': {  
'A': 'Ter apenas uma renda extra para pagar as contas',  
'B': 'Trabalhar de casa e largar o meu emprego atual',  
'C': 'Construir um negócio digital altamente lucrativo'  
}  
},  
{  
'id': 3,  
'texto': 'Qual é a sua experiência atual com marketing digital?',  
'opcoes': {  
'A': 'Zero, sou totalmente iniciante',  
'B': 'Conheço um pouco, mas sem resultados',  
'C': 'Já tenho experiência, mas quero escalar'  
}  
}  
\],  
'saude': \[  
{  
'id': 1,  
'texto': 'Qual é o seu principal objetivo de saúde atualmente?',  
'opcoes': {  
'A': 'Perder peso rapidamente',  
'B': 'Ganhar massa muscular',  
'C': 'Ter mais energia e disposição no dia a dia'  
}  
},  
{  
'id': 2,  
'texto': 'Como é a sua rotina de exercícios atual?',  
'opcoes': {  
'A': 'Não pratico nenhum exercício (sedentário)',  
'B': 'Pratico de 1 a 2 vezes por semana',  
'C': 'Pratico 3 ou mais vezes por semana'  
}  
}  
\]  
} 

AFFILIATE\_LINKS = {  
'renda\_extra': {  
'A': 'hotmart.com',  
'B': 'hotmart.com',  
'C': 'hotmart.com'  
},  
'saude': {  
'A': 'hotmart.com',  
'B': 'hotmart.com',  
'C': 'hotmart.com'  
}  
} 

@app.route('/')  
def index():  
return render\_template('index.html') 

@app.route('/quiz/')  
def iniciar\_quiz(categoria):  
if categoria not in QUIZZES:  
return redirect(url\_for('index')) 

session\['categoria'\] = categoria  
session\['respostas'\] = \[\]  
return redirect(url\_for('mostrar\_pergunta', pergunta\_id=1)) 

@app.route('/pergunta/int:pergunta\_id', methods=\['GET', 'POST'\])  
def mostrar\_pergunta(pergunta\_id):  
categoria = session.get('categoria')  
if not categoria or categoria not in QUIZZES:  
return redirect(url\_for('index')) 

perguntas = QUIZZES\[categoria\] 

if pergunta\_id > len(perguntas):  
return redirect(url\_for('mostrar\_resultado')) 

pergunta\_atual = perguntas\[pergunta\_id - 1\] 

if request.method == 'POST':  
resposta = request.form.get('resposta')  
if resposta:  
respostas = session.get('respostas', \[\])  
respostas.append(resposta)  
session\['respostas'\] = respostas  
return redirect(url\_for('mostrar\_pergunta', pergunta\_id=pergunta\_id + 1)) 

return render\_template('quiz.html', pergunta=pergunta\_atual, total=len(perguntas), atual=pergunta\_id) 

@app.route('/resultado')  
def mostrar\_resultado():  
categoria = session.get('categoria')  
respostas = session.get('respostas', \[\]) 

if not categoria or not respostas:  
return redirect(url\_for('index')) 

perfil = max(set(respostas), key=respostas.count) if respostas else 'A'  
link\_final = AFFILIATE\_LINKS.get(categoria, {}).get(perfil, '#') 

return render\_template('resultado.html', perfil=perfil, link\_checkout=link\_final, categoria=categoria) 

if **name** == '**main**':  
app.run(debug=True)