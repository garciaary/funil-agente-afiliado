import os
from flask import Flask, render_template, request, redirect, url_for, session

# Define os caminhos de template de forma segura
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'chave_secreta_para_sessoes_seguras'

# Estrutura de Quizzes Atualizada para Venda de Infoprodutos
QUIZZES = {
    'renda_extra': [
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
    ],
    'saude': [
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
    ]
}

# Links de afiliados configurados por categoria e resposta predominante
AFFILIATE_LINKS = {
    'renda_extra': {
        'A': 'https://hotmart.com',
        'B': 'https://hotmart.com',
        'C': 'https://hotmart.com'
    },
    'saude': {
        'A': 'https://hotmart.com',
        'B': 'https://hotmart.com',
        'C': 'https://hotmart.com'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<categoria>')
def iniciar_quiz(categoria):
    if categoria not in QUIZZES:
        return redirect(url_for('index'))
    
    session['categoria'] = categoria
    session['respostas'] = []
    return redirect(url_for('mostrar_pergunta', pergunta_id=1))

@app.route('/pergunta/<int:pergunta_id>', methods=['GET', 'POST'])
def mostrar_pergunta(pergunta_id):
    categoria = session.get('categoria')
    if not categoria or categoria not in QUIZZES:
        return redirect(url_for('index'))
    
    perguntas = QUIZZES[categoria]
    
    if pergunta_id > len(perguntas):
        return redirect(url_for('mostrar_resultado'))
        
    pergunta_atual = perguntas[pergunta_id - 1]
    
    if request.method == 'POST':
        resposta = request.form.get('resposta')
        if resposta:
            respostas = session.get('respostas', [])
            respostas.append(resposta)
            session['respostas'] = respostas
            return redirect(url_for('mostrar_pergunta', pergunta_id=pergunta_id + 1))
            
    return render_template('quiz.html', pergunta=pergunta_atual, total=len(perguntas), atual=pergunta_id)

@app.route('/resultado')
def mostrar_resultado():
    categoria = session.get('categoria')
    respostas = session.get('respostas', [])
    
    if not categoria or not respostas:
        return redirect(url_for('index'))
        
    perfil = max(set(respostas), key=respostas.count) if respostas else 'A'
    link_final = AFFILIATE_LINKS.get(categoria, {}).get(perfil, '#')
    
    return render_template('resultado.html', perfil=perfil, link_checkout=link_final, categoria=categoria)

if __name__ == '__main__':
    app.run(debug=True)
