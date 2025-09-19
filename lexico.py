import ply.lex as lex

# dicionário de palavras resevradas
p_reservadas = {
    'program':'PROGRAM',
    'var':'VAR',
    'begin':'BEGIN',
    'end':'END',
    'integer':'INTEGER',
    'boolean':'BOOLEAN',
    'false':'FALSE',
    'true':'TRUE',
    'read':'READ',
    'write':'WRITE',
    'while':'WHILE',
    'do':'DO',
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'div':'DIV',   
    'and':'AND',
    'or':'OR',
    'not':'NOT',
}

# tokens válidos
tokens = [
    'ID', # token utilizado para lidarmos com as palavras reservadas
    'NUMERO',# token para separar literais de nomes
    'EPAR', 
    'DPAR', 
    'PV',
    'IGUAL',
    'MQMQ',
    'MENORQUE',
    'MENORIGUAL',
    'MAIORQUE',
    'MAIORIGUAL',
    'MAIS',
    'MENOS',
    'VEZES',
    'DPIGUAL',
    'DP',
    'VIRG',
    'PF'
] + list(p_reservadas.values())

# regras para os tokens mais simples, sem ações
t_EPAR = r'\('
t_DPAR = r'\)'
t_PV = r';'
t_IGUAL = r'='
t_MQMQ = r'<>'
t_MENORQUE = r'<'
t_MAIORQUE = r'>'
t_MENORIGUAL = r'<='
t_MAIORIGUAL = r'>='
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DPIGUAL = r':='
t_DP = r':'
t_VIRG = r','
t_PF = r'\.'
t_ignore = ' \t' #regra para ignorar espaços e tabs

# regras para tokens com ações associadas

def t_ID(t): 
    
    # regex (ER)
    # A-Za-z -> qualquer letra maiúscula e minúscula de A a Z
    # A-Za-z0-9_ -> qualquer letra maiúscula e minúscula de A a Z, número de 0 a 9 e Underline (_)
    r'[A-Za-z][A-Za-z0-9_]*' 

    t.type = p_reservadas.get(t.value, 'ID') # verifica em p_reservadas uma chave igual ao lexema
    return t # retorna token da palavra reservada (se existir), ou token padrão ID

def t_NUMERO(t):

    # qualquer dígito numérico uma ou mais(+) vezes
    # "-" não é processado nesta fase
    r'\d+' 

    t.value = int(t.value) # converte a string para um inteiro
    return t # retorna token NUMBER

def t_newline(t): 
    r'\n+'
    t.lexer.lineno += len(t.value) # manter o número da linha correto


def t_error(t):
    print("ERRO: Símbolo '%s' linha '%d' na posição '%d' é ilegal" %(t.value[0],t.lexer.lineno, t.lexer.lexpos))
    t.lexer.skip(1)

lexico = lex.lex()