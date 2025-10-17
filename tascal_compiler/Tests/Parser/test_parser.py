import sys, os
from tascal_compiler.parser import parser

arquivo = sys.argv[1]
arquivo = os.path.join(os.path.dirname(__file__), arquivo)

with open(arquivo, "r") as f:
    data = f.read()

print("\n--- INICIANDO ANÁLISE SINTÁTICA ---\n")
parser.parse(data)
print("\n--- ANÁLISE FINALIZADA ---\n")
