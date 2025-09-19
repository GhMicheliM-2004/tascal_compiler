from lexico import lexico

teste = """
program p;
var a, b: integer;
begin
  a := 1;
  b := a + 2;
  write(a,b);
end.
"""

lexico.input(teste)

while True:
    tok = lexico.token()
    if not tok:
        break      # sem mais dados
    print(tok)