import ply.yacc as yacc
from tascal_compiler.lexer import tokens

# --------------------------------------
# Tabela de símbolos e erros semânticos
# --------------------------------------

tab_simbolos = {}
erros_semanticos = []


def semantico_reset():
    global tab_simbolos, erros_semanticos
    tab_simbolos = {}
    erros_semanticos = []


def erro_semantico(msg, lineno=None):
    if lineno:
        print(f"ERRO SEMÂNTICO na linha {lineno}: {msg}")
    else:
        print(f"ERRO SEMÂNTICO: {msg}")
    erros_semanticos.append(msg)


def instala_programa(nome, linha):
    if nome in tab_simbolos:
        erro_semantico(f"identificador de programa '{nome}' já declarado", linha)
    else:
        tab_simbolos[nome] = {"categoria": "programa", "tipo": None, "linha": linha}


def instala_variavel(nome, tipo, linha):
    if nome in tab_simbolos:
        erro_semantico(f"variável '{nome}' já declarada", linha)
    else:
        tab_simbolos[nome] = {"categoria": "variavel", "tipo": tipo, "linha": linha}


def busca_variavel(nome, linha):
    if nome not in tab_simbolos:
        erro_semantico(f"variável '{nome}' não declarada", linha)
        return None
    return tab_simbolos[nome]["tipo"]


def verifica_atribuicao(nome, tipo_expr, linha):
    if nome not in tab_simbolos:
        erro_semantico(f"variável '{nome}' não declarada", linha)
        return
    tipo_var = tab_simbolos[nome]["tipo"]
    if tipo_var != tipo_expr:
        erro_semantico(f"atribuição incompatível: variável '{nome}' é {tipo_var}, expressão é {tipo_expr}", linha)


def verifica_condicao(tipo, linha, contexto):
    if tipo != "boolean":
        erro_semantico(f"condição do {contexto} deve ser booleana (obtido {tipo})", linha)

# --------------------------------------
# Gramática Tascal (estilo parser_erros.py)
# --------------------------------------

def p_programa(p):
    """programa : PROGRAM ID PV bloco PF"""
    semantico_reset()
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
    """bloco : secao_decl_var comando_composto
             | comando_composto"""
    p[0] = None


def p_secao_decl_var(p):
    """secao_decl_var : VAR declaracao_var PV lista_decl_var
                      | VAR declaracao_var PV"""
    p[0] = None


def p_lista_decl_var(p):
    """lista_decl_var : declaracao_var PV lista_decl_var
                      | declaracao_var PV"""
    p[0] = None


def p_declaracao_var(p):
    """declaracao_var : lista_id DP tipo"""
    tipo = p[3].lower()
    for nome, linha in p[1]:
        instala_variavel(nome, tipo, linha)
    p[0] = None


def p_lista_id(p):
    """lista_id : ID
                | ID VIRG lista_id"""
    if len(p) == 2:
        p[0] = [(p[1], p.lineno(1))]
    else:
        p[0] = [(p[1], p.lineno(1))] + p[3]


def p_tipo(p):
    """tipo : INTEGER
            | BOOLEAN"""
    p[0] = p[1]


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
               | condicional
               | repeticao
               | leitura
               | escrita
               | comando_composto"""
    p[0] = None


def p_atribuicao(p):
    """atribuicao : ID DPIGUAL expressao"""
    nome = p[1]
    tipo_expr = p[3]
    verifica_atribuicao(nome, tipo_expr, p.lineno(2))
    p[0] = None


def p_condicional(p):
    """condicional : IF expressao THEN comando
                   | IF expressao THEN comando ELSE comando"""
    tipo_cond = p[2]
    verifica_condicao(tipo_cond, p.lineno(1), "if")
    p[0] = None


def p_repeticao(p):
    """repeticao : WHILE expressao DO comando"""
    tipo_cond = p[2]
    verifica_condicao(tipo_cond, p.lineno(1), "while")
    p[0] = None


def p_leitura(p):
    """leitura : READ EPAR lista_id DPAR"""
    for nome, linha in p[3]:
        if nome not in tab_simbolos:
            erro_semantico(f"variável '{nome}' não declarada em read()", linha)
    p[0] = None


def p_escrita(p):
    """escrita : WRITE EPAR lista_exp DPAR"""
    for tipo, linha in p[3]:
        if tipo not in ("integer", "boolean"):
            erro_semantico(f"write() recebeu tipo inválido '{tipo}'", linha)
    p[0] = None


def p_lista_exp(p):
    """lista_exp : expressao
                 | expressao VIRG lista_exp"""
    if len(p) == 2:
        p[0] = [(p[1], p.lineno(1))]
    else:
        p[0] = [(p[1], p.lineno(1))] + p[3]


def p_expressao(p):
    """expressao : expressao_simples
                 | expressao_simples relacao expressao_simples"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "boolean"
    p[0] = p[0] or None


def p_relacao(p):
    """relacao : IGUAL
               | DIFERENTE
               | MENORQUE
               | MENORIGUAL
               | MAIORQUE
               | MAIORIGUAL"""
    p[0] = None


def p_expressao_simples(p):
    """expressao_simples : termo
                         | expressao_simples MAIS termo
                         | expressao_simples MENOS termo
                         | expressao_simples OR termo"""
    p[0] = "integer" if len(p) > 2 and p[2] in ("MAIS", "MENOS") else "boolean" if len(p) > 2 else p[1]
    p[0] = p[0] or None


def p_termo(p):
    """termo : fator
             | termo VEZES fator
             | termo DIV fator
             | termo AND fator"""
    p[0] = "integer" if len(p) > 2 and p[2] in ("VEZES", "DIV") else "boolean" if len(p) > 2 else p[1]
    p[0] = p[0] or None


def p_fator(p):
    """fator : ID
             | NUMERO
             | TRUE
             | FALSE
             | EPAR expressao DPAR
             | NOT fator
             | MENOS fator"""
    p[0] = None


# --------------------------------------
# Tratamento de erros (estilo parser_erros.py)
# --------------------------------------

def p_secao_decl_var_error(p):
    """secao_decl_var : VAR error"""
    print(f"ERRO SINTÁTICO na linha {p.lineno(2)}: declaração de variáveis inválida")
    parser.errok()
    p[0] = None


def p_lista_comandos_error(p):
    """lista_comandos : lista_comandos error PV"""
    print(f"ERRO SINTÁTICO na linha {p.lineno(2)}: comando inválido (descartando até ';')")
    parser.errok()
    p[0] = None


def p_atribuicao_error(p):
    """atribuicao : ID DPIGUAL error"""
    print(f"ERRO SINTÁTICO na linha {p.lineno(3)}: expressão inválida à direita de ':='")
    parser.errok()
    p[0] = None


def p_fator_paren_error(p):
    """fator : EPAR error DPAR"""
    print(f"ERRO SINTÁTICO na linha {p.lineno(2)}: expressão entre parênteses inválida")
    parser.errok()
    p[0] = None


def p_error(p):
    if p is None:
        print("ERRO SINTÁTICO: fim de arquivo inesperado (EOF)")
    else:
        print(f"ERRO SINTÁTICO na linha {p.lineno}: token inesperado ({p.value!r})")
    p[0] = None


# --------------------------------------
# Construção do parser
# --------------------------------------
parser = yacc.yacc()
