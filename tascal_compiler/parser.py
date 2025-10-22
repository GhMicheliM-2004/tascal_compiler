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
    # (aqui você poderia adicionar nome do programa se quiser)
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
#  Regras sintáticas
# ==========================================

def p_programa(p):
    """programa : PROGRAM ID PV bloco PF"""
    instala_programa(p[2], p.lineno(2))
    print("Programa reconhecido com sucesso!")

    if erros_semanticos:
        print("\n--- ERROS SEMÂNTICOS ---")
        for e in erros_semanticos:
            print(" -", e)
    else:
        print("\nNenhum erro semântico encontrado.")
    p[0] = None


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
#  Expressões e operações
# ==========================================

def p_expressao(p):
    """expressao : expressao_simples
                 | expressao_simples relacao expressao_simples"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        op = p.slice[2].type
        t1 = p[1]
        t2 = p[3]

        if op in ("MENORQUE", "MENORIGUAL", "MAIORQUE", "MAIORIGUAL"):
            if t1 != "integer" or t2 != "integer":
                erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {t1} e {t2})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "boolean"
        elif op in ("IGUAL", "DIFERENTE"):  # MQMQ = <>
            if t1 != t2:
                erro_semantico(f"operador '{p[2]}' requer operandos do mesmo tipo (obtido {t1} e {t2})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "boolean"
        else:
            p[0] = None


def p_expressao_simples(p):
    """expressao_simples : termo
                         | expressao_simples MAIS termo
                         | expressao_simples MENOS termo
                         | expressao_simples OR termo"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        op = p.slice[2].type
        left = p[1]
        right = p[3]

        if op in ("MAIS", "MENOS"):
            if left != "integer" or right != "integer":
                erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "integer"
        elif op == "OR":
            if left != "boolean" or right != "boolean":
                erro_semantico(f"operador 'or' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "boolean"
        else:
            p[0] = None


def p_termo(p):
    """termo : fator
             | termo VEZES fator
             | termo DIV fator
             | termo AND fator"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        op = p.slice[2].type
        left = p[1]
        right = p[3]

        if op in ("VEZES", "DIV"):
            if left != "integer" or right != "integer":
                erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "integer"
        elif op == "AND":
            if left != "boolean" or right != "boolean":
                erro_semantico(f"operador 'and' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
                p[0] = None
            else:
                p[0] = "boolean"
        else:
            p[0] = None


def p_fator(p):
    """fator : ID
             | NUMERO
             | TRUE
             | FALSE
             | EPAR expressao DPAR
             | NOT fator
             | MENOS fator"""
    if len(p) == 2:
        tok = p[1]
        if isinstance(tok, int):
            p[0] = "integer"
        elif p.slice[1].type in ("TRUE", "FALSE"):
            p[0] = "boolean"
        elif p.slice[1].type == "ID":
            p[0] = busca_variavel(tok, p.lineno(1))
        else:
            p[0] = None

    elif len(p) == 4 and p.slice[1].type == "EPAR":
        p[0] = p[2]

    elif p.slice[1].type == "NOT":
        tipo_f = p[2]
        if tipo_f != "boolean":
            erro_semantico(f"operador 'not' requer expressão booleana (obtido {tipo_f})", p.lineno(1))
            p[0] = None
        else:
            p[0] = "boolean"

    elif p.slice[1].type == "MENOS":
        tipo_f = p[2]
        if tipo_f != "integer":
            erro_semantico(f"operador unário '-' requer expressão inteira (obtido {tipo_f})", p.lineno(1))
            p[0] = None
        else:
            p[0] = "integer"
    else:
        p[0] = None


def p_relacao(p):
    """relacao : IGUAL
               | DIFERENTE
               | MENORQUE
               | MENORIGUAL
               | MAIORQUE
               | MAIORIGUAL"""
    p[0] = p[1]


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático: fim de arquivo inesperado.")


# ==========================================
#  Construção do parser
# ==========================================
parser = yacc.yacc()
