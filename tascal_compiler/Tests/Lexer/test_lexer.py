# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script de teste para o analisador léxico do Tascal
import sys, os
from tascal_compiler.lexer import lexico

# Se não passar argumento, usa o arquivo padrão
arquivo = sys.argv[1] 
arquivo = os.path.join(os.path.dirname(__file__), arquivo)

# Lê o código-fonte
with open(arquivo, "r") as f:
    data = f.read()

print("========================================")
print("  ANÁLISE LÉXICA TASCAL  ")
print("========================================\n")
print(f"Arquivo: {os.path.basename(arquivo)}\n")

# Alimenta o analisador léxico
lexico.input(data)

# Itera sobre os tokens e imprime cada um
print("\n--- TOKENS RECONHECIDOS ---\n")
for token in lexico:
    print(f"{token.type:<12} -> {token.value}")

print("\n========================================")
print("        ANÁLISE FINALIZADA              ")  
print("========================================\n")
