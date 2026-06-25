import os  
from flask import Flask, render\_template, request, redirect, url\_for, session 

### Define os caminhos de template de forma segura

base\_dir = os.path.abspath(os.path.dirname(**file**))  
template\_dir = os.path.join(base\_dir, 'templates') 

app = Flask(**name**, template\_folder=template\_dir)  
app.secret\_key = 'chave\_secreta\_para\_sessoes\_seguras' 

### Estrutura de Quizzes Atualizada para Venda de Infoprodutos

QUIZZES = {  
'renda\_extra': \[  
{  
'id': 1,  
'texto': 'Qual área do mercado digital ou profissional você mais tem interesse em aprender?',  
'opcoes': {  
'A': 'Design de Unhas e Estética (Curso de Manicure Profissional)',  
'B': 'Inteligência Artificial e Produtividade (Curso de IA / ChatGPT)',  
'C': 'Finanças Pessoais e Investimentos (Organização Financeira)'  
}  
},  
{  
'id': 2,  
'texto': 'Qual é o seu principal objetivo ao adquirir esse treinamento?',  
'opcoes': {  
'A': 'Trabalhar da minha própria casa e criar uma nova profissão lucrativa',  
'B': 'Aumentar meus resultados e ganhar tempo no meu trabalho atual usando tecnologia',  
'C': 'Organizar minhas contas, sair das dívidas e começar a investir do zero'  
}  
}  
\],  
'saude': \[  
{  
'id': 1,  
'texto': 'Qual é o seu principal objetivo em relação ao seu corpo hoje?',  
'opcoes': {  
'A': 'Perder peso rapidamente de forma saudável (Reeducação Alimentar)',  
'B': 'Definir os músculos e ganhar condicionamento físico praticando exercícios',  
'C': 'Aprender receitas práticas e rápidas para a rotina corrida'  
}  
},  
{  
'id': 2,  
'texto': 'Qual é o maior obstáculo que te impede de alcançar sua meta de saúde?',  
'opcoes': {  
'A': 'Falta de conhecimento sobre alimentação correta (efeito sanfona)',  
'B': 'Falta de tempo para ir à academia todos os dias',  
'C': 'Não saber cozinhar pratos saudáveis que sejam saborosos'  
}  
}  
\]  
} 

### Links de afiliados configurados por categoria e resposta predominante

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