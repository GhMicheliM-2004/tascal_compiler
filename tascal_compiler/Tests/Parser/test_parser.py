# Script de teste para o analisador sintático e semântico do Tascal
# Executa a análise em um arquivo de código Tascal e exibe os resultados
import sys
import os
from tascal_compiler.parser import parser, erros_semanticos, semantico_reset
from tascal_compiler.lexer import lexico

def executar_teste(caminho_arquivo):

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo: # Abre o arquivo de código Tascal
        codigo = arquivo.read()

    print("========================================")
    print("  ANÁLISE SINTÁTICA + SEMÂNTICA TASCAL  ")
    print("========================================\n")
    print(f"Arquivo: {os.path.basename(caminho_arquivo)}\n")

    try:
        
        semantico_reset() # Reseta estado semântico antes da análise
        lexico.lineno = 1
        
        parser.parse(codigo, lexer=lexico) # Executa análise

    except Exception:
        None

    print("\n========================================")
    print("        ANÁLISE FINALIZADA              ")
    print("========================================\n")


def main():

    # Executa o analisador em um arquivo de teste informado via terminal
    # Exemplo: py -m tascal_compiler.Tests.Parser.test_parser tascal_compiler/Tests/ProgramasTascalTeste/PErr18.tascal
    arquivo = sys.argv[1] # Pega o arquivo do argumento de linha de comando
    executar_teste(arquivo) # Executa o teste no arquivo fornecido


if __name__ == "__main__":
    main()
