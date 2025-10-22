# import sys
# import os
# from parser import parser, erros_semanticos
# from lexer import lexico

# # ============================================
# # Teste integrado: análise sintática + semântica
# # ============================================

# # Caminho completo do arquivo de teste
# arquivo = sys.argv[1]
# arquivo = os.path.join(os.path.dirname(__file__), arquivo)

# with open(arquivo, "r") as f:
#         data = f.read()

# print("\n========================================")
# print("   ANÁLISE SINTÁTICA + SEMÂNTICA TASCAL ")
# print("========================================\n")

# # Executa o parser (que já faz a parte semântica internamente)
# parser.parse(data, lexer=lexico)

# print("\n========================================")
# print("         ANÁLISE FINALIZADA")
# print("========================================\n")

import sys
import os
from tascal_compiler.parser import parser, erros_semanticos
from tascal_compiler.lexer import lexer

# ===============================================
#    TESTE DO ANALISADOR SINTÁTICO E SEMÂNTICO
# ===============================================

def executar_teste(caminho_arquivo):
    """
    Executa a análise sintática + semântica de um arquivo .tas
    mostrando o resultado formatado.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("========================================")
    print("  ANÁLISE SINTÁTICA + SEMÂNTICA TASCAL  ")
    print("========================================\n")
    print(f"Arquivo: {os.path.basename(caminho_arquivo)}\n")

    try:
        # Reinicia o lexer e o parser
        lexer.lineno = 1
        parser.parse(codigo, lexer=lexer)
    except Exception as e:
        print(f"\nERRO durante a análise: {e}")

    print("\n========================================")
    print("        ANÁLISE FINALIZADA              ")
    print("========================================\n")


def main():
    """
    Executa o analisador em um arquivo de teste informado via terminal:
      Exemplo:
        py -m tascal_compiler.Tests.Parser.test_parser caminho_para_arquivo.tas
    """
    if len(sys.argv) < 2:
        print("Uso: py -m tascal_compiler.Tests.Parser.test_parser <arquivo.tas>")
        sys.exit(1)

    arquivo = sys.argv[1]
    executar_teste(arquivo)


if __name__ == "__main__":
    main()
