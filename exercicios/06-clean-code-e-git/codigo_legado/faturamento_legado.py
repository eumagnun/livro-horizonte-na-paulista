"""Isto é (propositalmente) um código ruim — o tipo de coisa que Bianca
descreveria como "camadas de código de 2005 por cima de processos de 1998".
Ele funciona, mas ninguém consegue entender o que faz só de olhar.

NÃO EDITE ESTE ARQUIVO. Ele existe só como referência de comportamento: seu
trabalho no Módulo 06 é reescrever uma versão limpa em `exercicio.py` que
produza EXATAMENTE o mesmo resultado.
"""


def proc(lst):
    d = {}
    for x in lst:
        a = x[0]
        t = x[1]
        n = x[2]
        c = x[3]
        if c == "9A" or c == "4F":
            if n not in d:
                d[n] = 0
            if t == "ESTORNO":
                v = -abs(a)
            else:
                v = abs(a)
            d[n] = d[n] + v
    return d
