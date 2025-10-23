import ply.yacc as yacc
from tascal_compiler.lexer import tokens

# ==========================================
#  Estruturas de dados semânticas
# ==========================================
tabela_variaveis = {}
erros_semanticos = []

# ==========================================
#  Funções auxiliares
# ==========================================
def semantico_reset():
    global tabela_variaveis, erros_semanticos
    tabela_variaveis = {}
    erros_semanticos = []

def erro_semantico(msg, linha):
    print(f"ERRO SEMÂNTICO na linha {linha}: {msg}")
    erros_semanticos.append(f"Linha {linha}: {msg}")

def instala_programa(nome, linha):
    pass

def instala_variavel(nome, tipo, linha):
    if nome in tabela_variaveis:
        erro_semantico(f"variável '{nome}' já declarada", linha)
    else:
        tabela_variaveis[nome] = tipo

def busca_variavel(nome, linha):
    if nome not in tabela_variaveis:
        erro_semantico(f"variável '{nome}' não declarada", linha)
        return None
    return tabela_variaveis[nome]

# ==========================================
#  Precedência (importante para evitar SR/RR)
# ==========================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE', 'MENORQUE', 'MENORIGUAL', 'MAIORQUE', 'MAIORIGUAL'),
    ('left', 'MAIS', 'MENOS'),
    ('left', 'VEZES', 'DIV'),
    ('right', 'NOT', 'UMINUS'),
)

# ==========================================
#  Regras sintáticas
# ==========================================

def p_programa(p):
    """programa : PROGRAM ID PV bloco PF"""
    instala_programa(p[2], p.lineno(2))

    if erros_semanticos:
        print("\nAnálise sintática concluída, mas com erros semânticos.")
    else:
        print("Programa reconhecido com sucesso (sintático e semântico)!")

    if erros_semanticos:
        print("\n--- ERROS SEMÂNTICOS ---")
        for e in erros_semanticos:
            print(" -", e)



def p_bloco(p):
    """bloco : declaracoes comando_composto"""
    p[0] = None


def p_declaracoes(p):
    """declaracoes : VAR declaracao_variaveis
                   | empty"""
    p[0] = None


def p_declaracao_variaveis(p):
    """declaracao_variaveis : lista_id DP tipo PV declaracao_variaveis
                            | lista_id DP tipo PV"""
    for nome in p[1]:
        instala_variavel(nome, p[3], p.lineno(1))
    p[0] = None


def p_lista_id(p):
    """lista_id : ID
                | ID VIRG lista_id"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_tipo(p):
    """tipo : INTEGER
            | BOOLEAN"""
    p[0] = p[1].lower()


def p_comando_composto(p):
    """comando_composto : BEGIN lista_comandos END"""
    p[0] = None


def p_lista_comandos(p):
    """lista_comandos : comando
                      | comando PV lista_comandos
                      | comando PV"""
    p[0] = None


def p_comando(p):
    """comando : atribuicao
               | comando_condicional
               | comando_enquanto
               | comando_leitura
               | comando_escrita
               | comando_composto
               | empty"""
    p[0] = None


def p_atribuicao(p):
    """atribuicao : ID DPIGUAL expressao"""
    tipo_var = busca_variavel(p[1], p.lineno(1))
    tipo_expr = p[3]

    if tipo_var and tipo_expr and tipo_var != tipo_expr:
        erro_semantico(f"atribuição incompatível: variável '{p[1]}' é {tipo_var}, expressão é {tipo_expr}", p.lineno(1))
    p[0] = None


def p_comando_condicional(p):
    """comando_condicional : IF expressao THEN comando
                           | IF expressao THEN comando ELSE comando"""
    if p[2] != "boolean":
        erro_semantico("condição do IF deve ser booleana", p.lineno(1))
    p[0] = None


def p_comando_enquanto(p):
    """comando_enquanto : WHILE expressao DO comando"""
    if p[2] != "boolean":
        erro_semantico("condição do WHILE deve ser booleana", p.lineno(1))
    p[0] = None


def p_comando_leitura(p):
    """comando_leitura : READ EPAR lista_id DPAR"""
    for nome in p[3]:
        if busca_variavel(nome, p.lineno(1)) is None:
            erro_semantico(f"variável '{nome}' não declarada", p.lineno(1))
    p[0] = None


def p_comando_escrita(p):
    """comando_escrita : WRITE EPAR lista_expressoes DPAR"""
    for tipo in p[3]:
        if tipo not in ("integer", "boolean"):
            erro_semantico(f"write() recebeu tipo inválido '{tipo}'", p.lineno(1))
    p[0] = None


def p_lista_expressoes(p):
    """lista_expressoes : expressao
                        | expressao VIRG lista_expressoes"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# ==========================================
#  Expressões (hierarquia clara)
# ==========================================

def p_expressao_or(p):
    """expressao : expressao OR expressao_and
                 | expressao_and"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        left, right = p[1], p[3]
        if left != "boolean" or right != "boolean":
            erro_semantico(f"operador 'or' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
        p[0] = "boolean"

def p_expressao_and(p):
    """expressao_and : expressao_and AND expressao_rel
                      | expressao_rel"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        left, right = p[1], p[3]
        if left != "boolean" or right != "boolean":
            erro_semantico(f"operador 'and' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
        p[0] = "boolean"

def p_expressao_rel(p):
    """expressao_rel : soma relacao soma
                     | soma"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        left, right = p[1], p[3]
        op = p[2]
        if op in ('<', '<=', '>', '>='):
            if left != "integer" or right != "integer":
                erro_semantico(f"operador '{op}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
            p[0] = "boolean"
        elif op in ('=', '<>'):
            if left != right:
                erro_semantico(f"operador '{op}' requer operandos do mesmo tipo (obtido {left} e {right})", p.lineno(2))
            p[0] = "boolean"

def p_soma(p):
    """soma : soma MAIS termo
            | soma MENOS termo
            | termo"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        left, right = p[1], p[3]
        if left != "integer" or right != "integer":
            erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
            p[0] = None
        else:
            p[0] = "integer"

def p_termo(p):
    """termo : termo VEZES fator
             | termo DIV fator
             | fator"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        left, right = p[1], p[3]
        if left != "integer" or right != "integer":
            erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
        p[0] = "integer"

def p_fator(p):
    """fator : ID
             | NUMERO
             | TRUE
             | FALSE
             | EPAR expressao DPAR
             | NOT fator
             | MENOS fator %prec UMINUS"""
    if len(p) == 2:
        if p.slice[1].type == "NUMERO":
            p[0] = "integer"
        elif p.slice[1].type in ("TRUE", "FALSE"):
            p[0] = "boolean"
        elif p.slice[1].type == "ID":
            tipo = busca_variavel(p[1], p.lineno(1))
            if tipo is None:
                tipo = "integer"
            p[0] = tipo
        else:
            p[0] = "integer"
    elif len(p) == 4 and p.slice[1].type == "EPAR":
        p[0] = p[2]
    elif p.slice[1].type == "NOT":
        if p[2] != "boolean":
            erro_semantico(f"operador 'not' requer expressão booleana (obtido {p[2]})", p.lineno(1))
        p[0] = "boolean"
    elif p.slice[1].type == "MENOS":
        if p[2] != "integer":
            erro_semantico(f"operador unário '-' requer expressão inteira (obtido {p[2]})", p.lineno(1))
        p[0] = "integer"

def p_relacao(p):
    """relacao : IGUAL
               | DIFERENTE
               | MENORQUE
               | MENORIGUAL
               | MAIORQUE
               | MAIORIGUAL"""
    # devolve o lexema do operador (por exemplo '<' ou '<=')
    p[0] = p[1]

def p_empty(p):
    """empty :"""
    pass

def p_error(p):
    if p:
        print(f"ERRO SINTÁTICO: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("ERRO SINTÁTICO: fim de arquivo inesperado.")

# ==========================================
#  Construção do parser
# ==========================================
parser = yacc.yacc()
