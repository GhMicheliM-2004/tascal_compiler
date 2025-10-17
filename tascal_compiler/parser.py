import ply.yacc as yacc
from tascal_compiler.lexer import tokens


# ===============================
# Regras sintáticas - Tascal
# ===============================

# Programa
def p_programa(p):
    'programa : PROGRAM ID PV bloco PF'
    print("Programa reconhecido com sucesso!")

# Bloco
def p_bloco(p):
    '''
    bloco : secao_decl_var comando_composto
          | comando_composto
    '''

# Seção de declaração de variáveis
def p_secao_decl_var(p):
    '''
    secao_decl_var : VAR declaracao_var PV lista_decl_var
                   | VAR declaracao_var PV
    '''

def p_lista_decl_var(p):
    '''
    lista_decl_var : declaracao_var PV lista_decl_var
                   | declaracao_var PV
    '''

def p_declaracao_var(p):
    'declaracao_var : lista_id DP tipo'

def p_lista_id(p):
    '''
    lista_id : ID
             | ID VIRG lista_id
    '''

def p_tipo(p):
    '''
    tipo : INTEGER
         | BOOLEAN
    '''

# Comando composto
def p_comando_composto(p):
    'comando_composto : BEGIN lista_comandos END'

def p_lista_comandos(p):
    '''
    lista_comandos : comando
                   | comando PV lista_comandos
                   | comando PV
    '''


# Comando
def p_comando(p):
    '''
    comando : atribuicao
            | condicional
            | repeticao
            | leitura
            | escrita
            | comando_composto
    '''

# Atribuição
def p_atribuicao(p):
    'atribuicao : ID DPIGUAL expressao'

# Condicional
def p_condicional(p):
    '''
    condicional : IF expressao THEN comando
                | IF expressao THEN comando ELSE comando
    '''

# Repetição
def p_repeticao(p):
    'repeticao : WHILE expressao DO comando'

# Leitura
def p_leitura(p):
    'leitura : READ EPAR lista_id DPAR'

# Escrita
def p_escrita(p):
    'escrita : WRITE EPAR lista_exp DPAR'

def p_lista_exp(p):
    '''
    lista_exp : expressao
              | expressao VIRG lista_exp
    '''

# Expressão
def p_expressao(p):
    '''
    expressao : expressao_simples
              | expressao_simples relacao expressao_simples
    '''

def p_relacao(p):
    '''
    relacao : IGUAL
            | DIFERENTE
            | MENORQUE
            | MENORIGUAL
            | MAIORQUE
            | MAIORIGUAL
    '''

def p_expressao_simples(p):
    '''
    expressao_simples : termo
                      | termo expressao_simples_op
    '''

def p_expressao_simples_op(p):
    '''
    expressao_simples_op : MAIS termo
                         | MENOS termo
                         | OR termo
                         | MAIS termo expressao_simples_op
                         | MENOS termo expressao_simples_op
                         | OR termo expressao_simples_op
    '''

def p_termo(p):
    '''
    termo : fator
          | fator termo_op
    '''

def p_termo_op(p):
    '''
    termo_op : VEZES fator
             | DIV fator
             | AND fator
             | VEZES fator termo_op
             | DIV fator termo_op
             | AND fator termo_op
    '''

def p_fator(p):
    '''
    fator : ID
          | NUMERO
          | logico
          | EPAR expressao DPAR
          | NOT fator
          | MENOS fator
    '''

def p_logico(p):
    '''
    logico : TRUE
           | FALSE
    '''

# Erros
def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático: fim de arquivo inesperado")

# Parser
parser = yacc.yacc()
