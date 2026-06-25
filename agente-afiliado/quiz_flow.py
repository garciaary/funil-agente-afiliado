### Estrutura do fluxo do quiz para direcionamento de produtos de afiliado

perguntas = {  
1: {  
"texto": "Qual área você deseja focar, aprender ou melhorar hoje?",  
"opcoes": {  
"A": "Estética & Beleza (Curso de Manicure Profissional)",  
"B": "Saúde & Fitness (E-books e Métodos de Emagrecimento)",  
"C": "Finanças & Organização (Aprender a investir ou sair das dívidas)",  
"D": "Tecnologia & Inovação (Aprender a usar Inteligência Artificial do zero)"  
}  
},  
2: {  
"texto": "Qual o seu principal objetivo ou dificuldade atual nessa área?",  
"opcoes": {  
"A": "Quero aprender uma nova profissão ou técnica para trabalhar e faturar",  
"B": "Falta de tempo na rotina corrida para focar nos resultados",  
"C": "Quero um passo a passo prático para iniciantes começarem do zero"  
}  
}  
} 

def obter\_pergunta(id\_pergunta):  
"""Retorna a pergunta correspondente ao ID informado."""  
return perguntas.get(id\_pergunta) 

def calcular\_total\_perguntas():  
"""Retorna a quantidade total de perguntas cadastradas."""  
return len(perguntas)