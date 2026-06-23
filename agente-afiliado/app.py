from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes'

# Estrutura de Quizzes por Categoria
QUIZZES = {
    'renda_extra': [
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
            'texto': 'Qual é a sua experiência atual com marketing digital?',
            'opcoes': {
                'A': 'Zero, sou totalmente iniciante',
                'B': 'Conheço um pouco, mas sem resultados',
                'C': 'Já tenho experiência, mas quero escalar'
            }
        }
    ],
    'saude': [
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
    ]
}

# Links de Afiliados separados por Categoria
AFFILIATE_LINKS = {
    'renda_extra': {
        'A': 'https://hotmart.com',
        'B': 'https://hotmart.com',
        'C': 'https://hotmart.com'
    },
    'saude': {
        'A': 'https://LINK_DE_EMAGRECIMENTO_A',
        'B': 'https://LINK_DE_EMAGRECIMENTO_B',
        'C': 'https://LINK_DE_EMAGRECIMENTO_C'
    }
}

@app.route('/')
def index():
    # Página inicial onde o usuário escolhe a categoria
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
            session['respostas'] = respuestas
            return redirect(url_for('mostrar_pergunta', pergunta_id=pergunta_id + 1))
            
    return render_template('quiz.html', pergunta=pergunta_atual, total=len(perguntas), atual=pergunta_id)

@app.route('/resultado')
def mostrar_resultado():
    categoria = session.get('categoria')
    respostas = session.get('respostas', [])
    
    if not categoria or not respostas:
        return redirect(url_for('index'))
        
    # Lógica simples para definir o perfil com base nas respostas (ex: mais comum)
    perfil = max(set(respostas), key=respostas.count) if respostas else 'A'
    
    # Busca o link correto com base na categoria escolhida e no perfil final
    link_final = AFFILIATE_LINKS.get(categoria, {}).get(perfil, '#')
    
    return render_template('resultado.html', perfil=perfil, link_checkout=link_final, categoria=categoria)

if __name__ == '__main__':
    app.run(debug=True)
