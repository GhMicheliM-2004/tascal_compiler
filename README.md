
# Como testar?

**Rode a partir da pasta raiz (tascal_compiler):**

py -m "patch+Arquivo" "Nome da entrada"

**Exemplo**

```bash
py -m tascal_compiler.Tests.Parser.test_parser ProgramasTascalTeste/P1.tascal
```

**Ou**

```bash
py -m tascal_compiler.Tests.Lexer.test_lexer ProgramasTascalTeste/P1.tascal
```


# Tascal Compiler

🛠️ **Compilador para a linguagem Tascal (Tiny Pascal)**

Este projeto é o **Trabalho Prático de Compiladores** da disciplina, implementando um compilador simples para a linguagem **Tascal** em **Python**, utilizando a biblioteca **PLY** (Python Lex-Yacc). O compilador abrange:

* Análise léxica (scanner)
* Análise sintática (parser)
* Verificações semânticas básicas (tipos, declarações)
* Mensagens de erro detalhadas (linha e tipo de erro)

---

## 🎯 Objetivos do Compilador

* Validar **programas Tascal**.
* Detectar e informar **erros léxicos, sintáticos e semânticos**.
* Executar programas simples interpretando as ações semânticas.
* Manter compatibilidade com a gramática definida para Tascal.

---

## 💡 Exemplos de Código Tascal

### Programa de exemplo 1: Soma de números

```pascal
program soma;
var
    x, y, z: integer;
begin
    read(x, y);
    z := x + y;
    write(z);
end.
```

**Saída esperada:**
Se o usuário digitar `2` e `3` na entrada, a saída será:

```
5
```

---

### Programa de exemplo 2: Uso de boolean

```pascal
program teste_boolean;
var
    a, b: boolean;
begin
    a := true;
    b := false;
    write(a, b);
end.
```

**Saída esperada:**

```
true false
```

---

## ⚙️ Estrutura do Projeto

```
tascal_compiler/
├── Tests                                                # Pasta contendo os arquivos test_ e instâncias
    ├── Lexer                                            # Pasta contendo os arquivos do Lexer
        ├── ProgramasTascalTeste                         # Instâncias
        ├── Tascal_Tester_Lexer_Invalido.tas             # Teste Inválido
        ├── Tascal_Tester_Lexer_Valido.tas               # Teste Válido
        ├── test_lexer.py                                # Testador de análise léxica
    ├── Parser                                           # Pasta contendo os arquivos do Parser
        ├── ProgramasTascalTeste                         # Instâncias
        ├── Tascal_Tester_Parser_Invalido.tas            # Teste Inválido
        ├── Tascal_Tester_Parser_Valido.tas              # Teste Válido
        ├── test_Parser.py                               # Testador de análise sintática e semântica
├── __init__.py                                          # Inicialização da pasta como pacote python
├── lex.py                                               # Arquivo gerado automáticamente pelo ply
├── lexer.py                                             # Analisador léxico (lexer)
├── parser.out                                           # Arquivo gerado automáticamente pelo ply
├── parser.py                                            # Analisador sintático e semântico (parser)
├── parsertab.py                                         # Arquivo gerado automáticamente pelo ply
├── yacc.py                                              # Funções auxiliares do ply.yacc                      .gitignore                                               # Arquivos ignorados
Especificação INF.pdf                                    # Especificação do projeto
README.md                                                # Este arquivo
```

---

## 💻 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/GhMicheliM-2004/tascal_compiler.git
cd tascal_compiler
```

2. Execute o compilador com um analisador por vez (lexer e parser), passando o arquivo Tascal como argumento:

```bash
py -m tascal_compiler.Tests.Lexer.test_lexer ProgramasTascalTeste/P1.tascal
# Retorna os tokens do arquivo, ou erros léxicos
```
```bash
py -m tascal_compiler.Tests.Parser.test_parser ProgramasTascalTeste/P1.tascal
# Realiza a análise sintática e semântica, imprimindo os erros caso algum seja obtido
```

3. Mensagens de erro serão exibidas com **linha e tipo de erro** (léxico, sintático ou semântico).
4. Programas válidos serão executados e exibirão os resultados na saída padrão.

---

## 📄 Referências

* APPEL, A. W.; GINSBURG, M. *Modern Compiler Implementation in C.* Cambridge University Press, 1998.
* KOWALTOWSKI, T. *Implementação de Linguagens de Programação.* Guanabara Dois, 1983.
* [PLY (Python Lex-Yacc) Documentation](https://ply.readthedocs.io/en/latest/index.html)
* DUDUSCRIPT. *pl0-ply: pl0 compiler written in python*. https://github.com/duduscript/pl0-ply]
* STRIDERDU. *Plycc: A compiler for C language using PLY [https://github.com/striderdu/Plycc]
* SMOHAMMADFY. *Compiler_PLY: Lexer and parser for compiler base like C/C++ with PLY python*[https://github.com/smohammadfy/Compiler_PLY]
