import ply.lex as lex

# Palavras reservadas
palavras_reservadas = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    'integer': 'INTEGER',
    'boolean': 'BOOLEAN',
    'false': 'FALSE',
    'true': 'TRUE',
    'read': 'READ',
    'write': 'WRITE',
    'while': 'WHILE',
    'do': 'DO',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'div': 'DIV',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
}

tokens = [
    'ID', 'NUMERO',
    'EPAR', 'DPAR', 'PV',
    'IGUAL', 'DIFERENTE',
    'MENORQUE', 'MENORIGUAL',
    'MAIORQUE', 'MAIORIGUAL',
    'MAIS', 'MENOS', 'VEZES',
    'DPIGUAL', 'DP', 'VIRG', 'PF'
] + list(palavras_reservadas.values())

t_EPAR = r'\('
t_DPAR = r'\)'
t_PV = r';'
t_IGUAL = r'='
t_DIFERENTE = r'<>'
t_MENORIGUAL = r'<='
t_MAIORIGUAL = r'>='
t_MENORQUE = r'<'
t_MAIORQUE = r'>'
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DPIGUAL = r':='
t_DP = r':'
t_VIRG = r','
t_PF = r'\.'
t_ignore = ' \t'

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\{[^}]*\}'
    print(f"ERRO LÉXICO: Comentários não são permitidos (linha {t.lineno})")

def t_error(t):
    print(f"ERRO LÉXICO: Símbolo ilegal '{t.value[0]}' na linha {t.lineno}")
    raise SyntaxError("Erro léxico encontrado")

lexico = lex.lex()
