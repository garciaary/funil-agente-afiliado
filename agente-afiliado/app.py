import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'evolucao-digital-change-me-in-production')

# ──────────────────────────────────────────────
# DADOS DOS PRODUTOS (configure seus links aqui)
# Substitua '#' pelos links reais de checkout
# ──────────────────────────────────────────────
PRODUTOS = {
    'profissional': {
        'A': {
            'badge': '💰 Perfil: Gerador de Renda',
            'titulo': 'Seu Plano para Aumentar a Renda',
            'intro': 'Com base nas suas respostas, você precisa de estratégias práticas para gerar renda extra ainda este mês.',
            'produto_titulo': 'Renda Extra Online — Do Zero ao Primeiro R$1.000',
            'produto_desc': 'Guia completo com 10 métodos validados para gerar renda extra sem precisar de investimento inicial.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'B': {
            'badge': '🤖 Perfil: Especialista em IA',
            'titulo': 'Domine a Inteligência Artificial',
            'intro': 'Você está no caminho certo. A IA vai transformar carreiras — e quem aprender agora sai na frente.',
            'produto_titulo': 'IA Para Iniciantes — Use ChatGPT e Ganhe Dinheiro',
            'produto_desc': 'Do básico ao avançado: aprenda a usar ferramentas de IA para trabalhar menos e ganhar mais.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'C': {
            'badge': '📈 Perfil: Investidor',
            'titulo': 'Sua Jornada Financeira Começa Aqui',
            'intro': 'Organize suas finanças e comece a investir com segurança — mesmo começando do zero.',
            'produto_titulo': 'Finanças Pessoais — Guia Completo Para Sair do Vermelho',
            'produto_desc': 'Passo a passo para organizar, economizar e começar a investir com qualquer salário.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'D': {
            'badge': '🏢 Perfil: Empreendedor',
            'titulo': 'Abra Seu Próprio Negócio',
            'intro': 'O momento é agora. Aprenda os passos reais para empreender com pouco investimento.',
            'produto_titulo': 'Do Ideia ao Faturamento — Guia do Empreendedor Digital',
            'produto_desc': 'Tudo o que você precisa saber para lançar, validar e vender online com baixo investimento.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
    },
    'saude': {
        'A': {
            'badge': '⚖️ Perfil: Emagrecimento',
            'titulo': 'Seu Plano de Reeducação Alimentar',
            'intro': 'Com base nos seus objetivos, você precisa de um método que alie alimentação e hábitos sustentáveis.',
            'produto_titulo': 'Método Emagrecer de Vez — Sem Sofrimento',
            'produto_desc': 'Programa completo de reeducação alimentar com cardápios prontos e suporte profissional.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'B': {
            'badge': '🥗 Perfil: Alimentação Saudável',
            'titulo': 'Receitas Fit Para o Seu Dia a Dia',
            'intro': 'Seu maior aliado será a praticidade na cozinha — receitas rápidas, gostosas e que emagrecem.',
            'produto_titulo': 'Guia Prático de Receitas Fit',
            'produto_desc': '100+ receitas saudáveis com lista de compras semanal e preparo em até 20 minutos.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'C': {
            'badge': '🏋️ Perfil: Treino em Casa',
            'titulo': 'Treine Sem Sair de Casa!',
            'intro': 'Você precisa de treinos eficientes que se encaixem na sua rotina — sem academia e sem equipamentos.',
            'produto_titulo': 'Treino em Casa — 21 Dias de Transformação',
            'produto_desc': 'Programa completo com vídeos, planilha de treino e acompanhamento de evolução.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'D': {
            'badge': '😴 Perfil: Energia e Disposição',
            'titulo': 'Recupere Sua Energia Total',
            'intro': 'A falta de energia afeta tudo: trabalho, relacionamento, saúde. Aprenda a recuperar sua disposição.',
            'produto_titulo': 'Despertar — Protocolo de Saúde e Energia',
            'produto_desc': 'Guia completo de hábitos, alimentação e rotina para recuperar energia em 14 dias.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
    },
    'estetica': {
        'A': {
            'badge': '💆 Perfil: Cuidados com a Pele',
            'titulo': 'Domine o Skincare Profissional',
            'intro': 'Aprenda a cuidar da pele com técnicas de quem entende — e transforme isso em renda extra.',
            'produto_titulo': 'Curso Completo de Estética Facial',
            'produto_desc': 'Skincare, limpeza de pele, tratamentos e protocolos profissionais com certificado.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'B': {
            'badge': '💄 Perfil: Maquiagem',
            'titulo': 'Torne-se uma Maquiadora Profissional',
            'intro': 'A maquiagem é uma das áreas mais lucrativas da estética. Aprenda técnicas que cobram alto.',
            'produto_titulo': 'Masterclass de Maquiagem Profissional',
            'produto_desc': 'Técnicas de maquiagem para noivas, eventos e dia a dia com certificado incluso.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'C': {
            'badge': '💅 Perfil: Micropigmentação',
            'titulo': 'Micropigmentação — Uma Profissão de Sucesso',
            'intro': 'Sobrancelha, lábios e olhos: aprenda a técnica mais cobrada do mercado de beleza.',
            'produto_titulo': 'Curso de Micropigmentação Completo',
            'produto_desc': 'Do básico ao avançado: design, pigmentação e técnicas de longa duração.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'D': {
            'badge': '💇 Perfil: Cabelos',
            'titulo': 'Transforme Carreiras com Cabelo',
            'intro': 'Coloração, corte e tratamento: domine as técnicas que fazem o sucesso do salão.',
            'produto_titulo': 'Curso de Cabelereiro(a) Profissional',
            'produto_desc': 'Técnicas de corte, coloração, tratamento capilar e atendimento personalizado.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
    },
    'espiritualidade': {
        'A': {
            'badge': '📖 Perfil: Buscador da Fé',
            'titulo': 'Aprofunde Sua Fé com Conteúdo de Qualidade',
            'intro': 'Você está em busca de um relacionamento mais profundo com Deus. Separamos os melhores e-books para essa jornada.',
            'produto_titulo': 'E-book: Devocional Diário — 365 Reflexões Bíblicas',
            'produto_desc': 'Um guia devocional completo para você ter um momento diário com Deus, com reflexões práticas.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'B': {
            'badge': '🕊️ Perfil: Buscador de Propósito',
            'titulo': 'Encontre Paz Interior e Seu Propósito',
            'intro': 'A espiritualidade é o alicerce de tudo. Um guia para descobrir sua identidade em Deus.',
            'produto_titulo': 'E-book: Propósito de Vida — Descubra Para Que Você Foi Criado',
            'produto_desc': 'Um guia espiritual e prático para entender sua missão e viver com significado real.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'C': {
            'badge': '🙌 Perfil: Líder Espiritual',
            'titulo': 'Fortaleça Sua Família e Sua Liderança',
            'intro': 'Um líder começa dentro de casa. Conteúdos que unem fé, família e missão de forma prática.',
            'produto_titulo': 'E-book: Família no Centro — Criando um Lar com Fé e Propósito',
            'produto_desc': 'Guia completo para fortalecer laços familiares, exercer liderança cristã e criar filhos com valores.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
        'D': {
            'badge': '✝️ Perfil: Discípulo na Prática',
            'titulo': 'Viva a Fé no Dia a Dia',
            'intro': 'A vida cristã se constrói com hábitos. Um e-book para criar disciplinas espirituais que funcionam.',
            'produto_titulo': 'E-book: Hábitos do Discípulo — 30 Dias de Disciplina Espiritual',
            'produto_desc': 'Programa de 30 dias com desafios práticos, reflexões bíblicas e exercícios espirituais.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        },
    },
}

# ──────────────────────────────────────────────
# BANCO DE DADOS — Tracking de respostas e emails
# ──────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')


def get_db():
    """Retorna conexão com o banco SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas se não existirem."""
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            perfil TEXT NOT NULL,
            email TEXT,
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()


init_db()


# ──────────────────────────────────────────────
# ROTAS
# ──────────────────────────────────────────────
@app.route('/')
def index():
    """Página inicial com categorias."""
    return render_template('index.html')


@app.route('/quiz')
def quiz():
    """Página do quiz."""
    categoria = request.args.get('categoria', '')
    return render_template('quiz.html', categoria_inicial=categoria)


@app.route('/email-form')
def email_form():
    """Exibe o formulário de captura de email."""
    categoria = request.args.get('categoria', '')
    perfil = request.args.get('perfil', '')
    utm_source = request.args.get('utm_source', '')
    utm_medium = request.args.get('utm_medium', '')
    utm_campaign = request.args.get('utm_campaign', '')
    return render_template('email.html', categoria=categoria, perfil=perfil,
                           utm_source=utm_source, utm_medium=utm_medium, utm_campaign=utm_campaign)


@app.route('/email', methods=['POST'])
def email_capture():
    """Recebe o email + respostas do quiz, salva no banco, redireciona para resultado."""
    categoria = request.form.get('categoria', '')
    perfil = request.form.get('perfil', '')
    email = request.form.get('email', '').strip()

    # Dados UTM (preservados via hidden fields no form)
    utm_source = request.form.get('utm_source', '')
    utm_medium = request.form.get('utm_medium', '')
    utm_campaign = request.form.get('utm_campaign', '')

    # Salvar no banco
    conn = get_db()
    conn.execute(
        'INSERT INTO quizzes (categoria, perfil, email, utm_source, utm_medium, utm_campaign) VALUES (?, ?, ?, ?, ?, ?)',
        (categoria, perfil, email or None, utm_source, utm_medium, utm_campaign)
    )
    conn.commit()
    conn.close()

    # Salvar na sessão para o resultado usar
    session['categoria'] = categoria
    session['perfil'] = perfil

    return redirect(url_for('resultado'))


@app.route('/resultado')
def resultado():
    """Exibe o resultado baseado nas respostas do quiz."""
    # Pegar da sessão (salvo pelo /email) ou fallback para query params
    categoria = session.get('categoria', '') or request.args.get('categoria', '')
    perfil = session.get('perfil', '') or request.args.get('perfil', '')

    # Validar valores
    categorias_validas = set(PRODUTOS.keys())
    perfis_validos = {'A', 'B', 'C', 'D'}
    if categoria not in categorias_validas or perfil not in perfis_validos:
        return redirect(url_for('index'))

    # Buscar produto correspondente
    produto = PRODUTOS.get(categoria, {}).get(perfil)
    if not produto:
        # Fallback genérico
        produto = {
            'badge': '🎯 Seu Resultado',
            'titulo': 'Encontramos o Conteúdo Ideal Para Você',
            'intro': 'Com base nas suas respostas, separamos o melhor treinamento para o seu perfil.',
            'produto_titulo': 'Conteúdo Digital Recomendado',
            'produto_desc': 'Acesse agora e comece sua transformação.',
            'checkout_link': '#CONFIGURAR_LINK_AQUI',
        }

    return render_template('resultado.html', produto=produto)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
