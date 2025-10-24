# Script do analisador sintático e semântico do Tascal
# Realiza verificação de tipos, declarações e usos de variáveis
# Gera mensagens de erro semântico detalhadas
import ply.yacc as yacc
from tascal_compiler.lexer import tokens

tabela_variaveis = {} # Tabela de símbolos para variáveis
erros_semanticos = [] # Lista de erros semânticos encontrados

def semantico_reset(): # Reseta o estado semântico
    global tabela_variaveis, erros_semanticos
    tabela_variaveis = {}
    erros_semanticos = []

def erro_semantico(msg, linha): # Registra um erro semântico
    print(f"ERRO SEMÂNTICO na linha {linha}: {msg}")
    erros_semanticos.append(f"Linha {linha}: {msg}")

def instala_programa(nome, linha): # Registra o programa principal
    pass 

def instala_variavel(nome, tipo, linha): # Registra uma variável na tabela de símbolos
    if nome in tabela_variaveis:
        erro_semantico(f"variável '{nome}' já declarada", linha) # Erro se redeclarada
    else:
        tabela_variaveis[nome] = tipo # Adiciona à tabela

def busca_variavel(nome, linha):
    if nome not in tabela_variaveis:
        erro_semantico(f"variável '{nome}' não declarada", linha)
        return None
    return tabela_variaveis[nome]

precedence = ( # Define precedência dos operadores para análise correta
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE', 'MENORQUE', 'MENORIGUAL', 'MAIORQUE', 'MAIORIGUAL'),
    ('left', 'MAIS', 'MENOS'),
    ('left', 'VEZES', 'DIV'),
    ('right', 'NOT', 'UMINUS'),
)

def p_programa(p): # Regra principal do programa, serve para iniciar a análise e finalizar
    """programa : PROGRAM ID PV bloco PF"""
    instala_programa(p[2], p.lineno(2))

    if erros_semanticos: # Se houver erros semânticos, informa
        print("\nAnálise sintática concluída, mas com erros semânticos.") # Informa conclusão com erros
    else: 
        print("Programa reconhecido com sucesso (sintático e semântico)!") # Informa sucesso

def p_bloco(p): # Regra do bloco principal do programa, serve para agrupar declarações e comandos
    """bloco : declaracoes comando_composto"""
    p[0] = None

def p_declaracoes(p): # Regra para declarações de variáveis
    """declaracoes : VAR declaracao_variaveis
                   | empty"""
    p[0] = None

def p_declaracao_variaveis(p): # Regra para declaração de variáveis, dessa vez com suporte a múltiplas variáveis
    """declaracao_variaveis : lista_id DP tipo PV declaracao_variaveis
                            | lista_id DP tipo PV"""
    
    for nome in p[1]: # Instala cada variável declarada
        instala_variavel(nome, p[3], p.lineno(1))
    p[0] = None

def p_lista_id(p): # Regra para lista de identificadores (variáveis)
    """lista_id : ID
                | ID VIRG lista_id"""
    
    if len(p) == 2: # Se o len for 2, é apenas um ID
        p[0] = [p[1]] 
    else: # Senão, é uma lista
        p[0] = [p[1]] + p[3]

def p_tipo(p): # Regra para tipos de variáveis
    """tipo : INTEGER
            | BOOLEAN"""
    p[0] = p[1].lower() # Retorna o tipo em minúsculo (lower)

def p_comando_composto(p): # Regra para comandos compostos (blocos de comandos)
    """comando_composto : BEGIN lista_comandos END"""
    p[0] = None

def p_lista_comandos(p): # Regra para lista de comandos, ou seja, múltiplos comandos separados
    """lista_comandos : comando
                      | comando PV lista_comandos
                      | comando PV"""
    p[0] = None

def p_comando(p): # Regra para comandos individuais
    """comando : atribuicao
               | comando_condicional
               | comando_enquanto
               | comando_leitura
               | comando_escrita
               | comando_composto
               | empty"""
    p[0] = None


def p_atribuicao(p): # Regra para atribuição
    """atribuicao : ID DPIGUAL expressao"""
    tipo_var = busca_variavel(p[1], p.lineno(1)) # Tipo da variável faz busca na tabela de símbolos
    tipo_expr = p[3] # Tipo da expressão é retornado pela regra de expressão

    if tipo_var and tipo_expr and tipo_var != tipo_expr: # Verifica compatibilidade de tipos
        erro_semantico(f"atribuição incompatível: variável '{p[1]}' é {tipo_var}, expressão é {tipo_expr}", p.lineno(1))
    p[0] = None

def p_comando_condicional(p): # Regra para comando condicional (if-else)
    """comando_condicional : IF expressao THEN comando
                           | IF expressao THEN comando ELSE comando"""
    if p[2] != "boolean":
        erro_semantico("condição do IF deve ser booleana", p.lineno(1))
    p[0] = None

def p_comando_enquanto(p): # Regra para comando repetição (while)
    """comando_enquanto : WHILE expressao DO comando"""
    if p[2] != "boolean":
        erro_semantico("condição do WHILE deve ser booleana", p.lineno(1))
    p[0] = None

def p_comando_leitura(p): # Regra para comando de leitura (read)
    """comando_leitura : READ EPAR lista_id DPAR"""
    for nome in p[3]:
        if busca_variavel(nome, p.lineno(1)) is None:
            erro_semantico(f"variável '{nome}' não declarada", p.lineno(1))
    p[0] = None

def p_comando_escrita(p): # Regra para comando de escrita (write)
    """comando_escrita : WRITE EPAR lista_expressoes DPAR"""
    for tipo in p[3]:
        if tipo not in ("integer", "boolean"):
            erro_semantico(f"write() recebeu tipo inválido '{tipo}'", p.lineno(1))
    p[0] = None

def p_lista_expressoes(p): # Regra para lista de expressões em comandos de escrita
    """lista_expressoes : expressao
                        | expressao VIRG lista_expressoes"""
    if len(p) == 2: # Se len for 2, é apenas uma expressão
        p[0] = [p[1]]
    else: # Senão, é uma lista
        p[0] = [p[1]] + p[3]

def p_expressao_or(p): # Regra para expressão com operador 'or'
    """expressao : expressao OR expressao_and
                 | expressao_and"""
    if len(p) == 2: # Se len for 2, é apenas uma expressão_and
        p[0] = p[1]
    else: # Senão, é uma expressão com 'or'
        left, right = p[1], p[3] # São os operandos, respectivamente à esquerda e direita, que recebem o operador
        if left != "boolean" or right != "boolean":
            erro_semantico(f"operador 'or' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
        p[0] = "boolean"

def p_expressao_and(p): # Regra para expressão com operador 'and'
    """expressao_and : expressao_and AND expressao_rel
                      | expressao_rel"""
    if len(p) == 2: # Se len for 2, é apenas uma expressão_rel
        p[0] = p[1]
    else: # Senão, é uma expressão com 'and'
        left, right = p[1], p[3] # São os operandos, respectivamente à esquerda e direita, que recebem o operador
        if left != "boolean" or right != "boolean":
            erro_semantico(f"operador 'and' requer operandos booleanos (obtido {left} e {right})", p.lineno(2))
        p[0] = "boolean"

def p_expressao_rel(p): # Regra para expressão com operadores relacionais
    """expressao_rel : soma relacao soma
                     | soma"""
    if len(p) == 2: # Se len for 2, é apenas uma soma
        p[0] = p[1]
    else: # Senão, é uma expressão relacional
        left, right = p[1], p[3] # São os operandos, respectivamente à esquerda e direita, que recebem o operador
        op = p[2]
        if op in ('<', '<=', '>', '>='): # Operadores relacionais que precisam de operandos inteiros
            if left != "integer" or right != "integer":
                erro_semantico(f"operador '{op}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
            p[0] = "boolean"
        elif op in ('=', '<>'): # Operadores relacionais que precisam de operandos do mesmo tipo
            if left != right:
                erro_semantico(f"operador '{op}' requer operandos do mesmo tipo (obtido {left} e {right})", p.lineno(2))
            p[0] = "boolean"

def p_soma(p): # Regra para expressão de soma e subtração 
    """soma : soma MAIS termo
            | soma MENOS termo
            | termo"""
    if len(p) == 2: # Se len for 2, é apenas um termo
        p[0] = p[1]
    else: # Senão, é uma expressão de soma ou subtração
        left, right = p[1], p[3]
        if left != "integer" or right != "integer":
            erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
            p[0] = None
        else:
            p[0] = "integer"

def p_termo(p): # Regra para expressão de multiplicação e divisão
    """termo : termo VEZES fator
             | termo DIV fator
             | fator"""
    if len(p) == 2: # Se len for 2, é apenas um fator
        p[0] = p[1]
    else: # Senão, é uma expressão de multiplicação ou divisão
        left, right = p[1], p[3]
        if left != "integer" or right != "integer":
            erro_semantico(f"operador '{p[2]}' requer operandos inteiros (obtido {left} e {right})", p.lineno(2))
        p[0] = "integer"

def p_fator(p): # Regra para fator (número, variável, expressão entre parênteses, negação, ou menos unário)
    """fator : ID
             | NUMERO
             | TRUE
             | FALSE
             | EPAR expressao DPAR
             | NOT fator
             | MENOS fator %prec UMINUS"""
    if len(p) == 2: # Se len for 2, é um ID, número ou booleano
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
    elif len(p) == 4 and p.slice[1].type == "EPAR": # Elif para expressão entre parênteses, retorna o tipo da expressão interna
        p[0] = p[2]
    elif p.slice[1].type == "NOT":
        if p[2] != "boolean":
            erro_semantico(f"operador 'not' requer expressão booleana (obtido {p[2]})", p.lineno(1))
        p[0] = "boolean"
    elif p.slice[1].type == "MENOS":
        if p[2] != "integer":
            erro_semantico(f"operador unário '-' requer expressão inteira (obtido {p[2]})", p.lineno(1))
        p[0] = "integer"

def p_relacao(p): # Regra para operadores relacionais, como =, <>, <, <=, >, >=
    """relacao : IGUAL
               | DIFERENTE
               | MENORQUE
               | MENORIGUAL
               | MAIORQUE
               | MAIORIGUAL"""
    # Devolve o lexema do operador (por exemplo '<' ou '<=')
    p[0] = p[1]

def p_empty(p): # Regra para produção vazia
    """empty :"""
    pass

def p_error(p): # Função de tratamento de erros sintáticos
    if p:
        print(f"ERRO SINTÁTICO: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("ERRO SINTÁTICO: fim de arquivo inesperado.")

#  Construção do parser
parser = yacc.yacc()
