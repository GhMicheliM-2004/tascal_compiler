
# Como testar?

**Rode a partir da pasta raiz:**

python -m "patch+Arquivo" "Nome da entrada"

**Exemplo**

python -m tascal_compiler.Tests.Lexer.test_lexer Tascal_Tester_Lexer_InValido.tas

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
├── lexico.py            # Analisador léxico (scanner)
├── sintatico.py         # Analisador sintático (parser)
├── semantico.py         # Verificações semânticas e interpretação
├── main.py              # Script principal para executar o compilador
├── teste_lexico.py      # Testes do lexer
├── teste_sintatico.py   # Testes do parser
├── README.md            # Este arquivo
└── .gitignore           # Arquivos ignorados
```

---

## 💻 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/GhMicheliM-2004/tascal_compiler.git
cd tascal_compiler
```

2. Execute o compilador passando o arquivo Tascal como argumento:

```bash
python main.py exemplos/soma.tas
```

3. Mensagens de erro serão exibidas com **linha e tipo de erro** (léxico, sintático ou semântico).
4. Programas válidos serão executados e exibirão os resultados na saída padrão.

---

## 🧪 Rodando os Testes

```bash
python -m unittest teste_lexico.py
python -m unittest teste_sintatico.py
```

Isso verifica se o lexer e parser estão funcionando corretamente.

---

## 📄 Referências

* APPEL, A. W.; GINSBURG, M. *Modern Compiler Implementation in C.* Cambridge University Press, 1998.
* KOWALTOWSKI, T. *Implementação de Linguagens de Programação.* Guanabara Dois, 1983.
* [PLY (Python Lex-Yacc) Documentation](https://ply.readthedocs.io/en/latest/index.html)
