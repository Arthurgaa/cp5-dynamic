
"""
Integrantes:
Arthur Galvão Alves - RM554462
Henrique Ignacio Bartalo - 555274
Gustavo Henrique Martins - RM556956
----------------
Quatro abordagens para o problema de Troca de Moedas (Coin Change):
  1) Guloso (interativo)
  2) Recursivo puro (sem memorização)
  3) Recursivo com memoização (Top-Down)
  4) Programação Dinâmica (Bottom-Up)
"""

from functools import lru_cache
from math import inf
from typing import Iterable, List

Impossible = -1  # valor de retorno para impossibilidade

def _validate_inputs(M: int, moedas: Iterable[int]) -> List[int]:
    """
    Valida entradas comuns e retorna as moedas únicas e positivas.

    - M deve ser um inteiro >= 0.
    - 'moedas' deve conter inteiros positivos (descarta duplicados e zeros/negativos).

    Retorna a lista de moedas válidas (únicas) não ordenadas.
    Lança ValueError para entradas inválidas de tipo/semântica.
    """
    if not isinstance(M, int):
        raise ValueError("M deve ser inteiro.")
    if M < 0:
        raise ValueError("M deve ser >= 0.")

    try:
        moedas_list = list(moedas)
    except TypeError:
        raise ValueError("'moedas' deve ser um iterável de inteiros positivos.")

    if len(moedas_list) == 0:
        return []

    try:
        moedas_list = [int(x) for x in moedas_list]
    except Exception as e:
        raise ValueError("'moedas' deve conter apenas inteiros.") from e

    moedas_list = [m for m in set(moedas_list) if m > 0]
    return moedas_list


def qtdeMoedas(M: int, moedas: Iterable[int]) -> int:
    """
    Calcula a quantidade mínima de moedas por uma estratégia **gulosa** (iterativa).

    A estratégia escolhe repetidamente a maior moeda possível <= restante.
    Observação: para sistemas de moedas gerais, o guloso **não garante** a solução ótima.

    Parâmetros
    ----------
    M : int
        Montante alvo (>= 0).
    moedas : Iterable[int]
        Conjunto de valores das moedas (inteiros positivos, quantidade ilimitada).

    Retorno
    -------
    int
        Mínimo de moedas encontrado pelo método guloso, ou -1 se não for possível formar M.

    Complexidade (teórica)
    ----------------------
    - Tempo:
      * Ordenação das moedas: O(k log k), k = número de tipos de moedas.
      * Loop guloso: O(k + a), onde 'a' é a quantidade de moedas efetivamente usadas.
      * No geral: O(k log k + k + a) = O(k log k + a); Ω(a) (casos com moedas já ordenadas e poucas iterações);
        Θ(k log k + a) quando sempre reordenamos e usamos 'a' moedas.
    - Espaço: O(1) além da ordenação (se in-place) / O(k) se considerarmos a cópia ordenada.
    """
    moedas = _validate_inputs(M, moedas)
    if M == 0:
        return 0
    if not moedas:
        return Impossible

    # Guloso: ordena desc e pega o máximo sempre que possível
    moedas.sort(reverse=True)
    restante = M
    usados = 0

    for m in moedas:
        if m <= 0:
            continue
        if restante <= 0:
            break
        qtd = restante // m
        usados += qtd
        restante -= qtd * m

    return usados if restante == 0 else Impossible


def qtdeMoedasRec(M: int, moedas: Iterable[int]) -> int:
    """
    Calcula a quantidade mínima de moedas via **recursão pura** (sem memoização).

    Define f(M) = min_{m in moedas, m<=M} (1 + f(M - m)), com f(0) = 0.
    Se nenhum caminho forma M, retorna -1.

    Parâmetros
    ----------
    M : int
    moedas : Iterable[int]

    Retorno
    -------
    int
        Quantidade mínima de moedas, ou -1 se impossível.

    Complexidade (teórica)
    ----------------------
    - Tempo (pior caso): **exponencial**, ~ O(k^M) (árvore de recursão com ramificação k e profundidade até M).
      Ω(1) quando M=0 (caso base) ou M está diretamente nas moedas e escolhido primeiro.
      Θ não é prática aqui por depender fortemente de sobreposição e poda inexistentes.
    - Espaço: O(M) devido à profundidade da pilha recursiva.
    """
    moedas = _validate_inputs(M, moedas)
    if M == 0:
        return 0
    if not moedas:
        return Impossible

    def rec(x: int) -> int:
        if x == 0:
            return 0
        melhor = inf
        for m in moedas:
            if m <= x:
                sub = rec(x - m)
                if sub != Impossible:
                    melhor = min(melhor, 1 + sub)
        return melhor if melhor != inf else Impossible

    return rec(M)


def qtdeMoedasRecMemo(M: int, moedas: Iterable[int]) -> int:
    """
    Calcula a quantidade mínima de moedas via **recursão com memoização (Top-Down)**.

    Usa um cache para armazenar f(x) = menor nº de moedas para atingir x.

    Parâmetros
    ----------
    M : int
    moedas : Iterable[int]

    Retorno
    -------
    int
        Quantidade mínima de moedas, ou -1 se impossível.

    Complexidade (teórica)
    ----------------------
    - Tempo: O(k * M), pois cada subproblema f(x) (0..M) é resolvido uma única vez
             e, para cada x, iteramos por k moedas.
      Ω(M) quando k é constante e todos os subproblemas precisam ser visitados.
      Θ(k * M) no caso usual (tabelas densas).
    - Espaço: O(M) para o cache + O(M) de pilha no pior caso => O(M).
    """
    moedas = _validate_inputs(M, moedas)
    if M == 0:
        return 0
    if not moedas:
        return Impossible

    @lru_cache(maxsize=None)
    def rec(x: int) -> int:
        if x == 0:
            return 0
        melhor = inf
        for m in moedas:
            if m <= x:
                sub = rec(x - m)
                if sub != Impossible:
                    melhor = min(melhor, 1 + sub)
        return melhor if melhor != inf else Impossible

    return rec(M)


def qtdeMoedasPD(M: int, moedas: Iterable[int]) -> int:
    """
    Calcula a quantidade mínima de moedas via **Programação Dinâmica Bottom-Up**.

    dp[i] = menor nº de moedas para formar o montante i.
    Transição: dp[i] = min_{m in moedas, m<=i} (1 + dp[i - m]), com dp[0] = 0.

    Parâmetros
    ----------
    M : int
    moedas : Iterable[int]

    Retorno
    -------
    int
        Quantidade mínima de moedas, ou -1 se impossível.

    Complexidade (teórica)
    ----------------------
    - Tempo: O(k * M) (dois loops aninhados: montante x moedas).
      Ω(M) quando k é constante e todos os montantes são visitados.
      Θ(k * M) tipicamente.
    - Espaço: O(M) para o vetor dp.
    """
    moedas = _validate_inputs(M, moedas)
    if M == 0:
        return 0
    if not moedas:
        return Impossible

    dp = [inf] * (M + 1)
    dp[0] = 0

    for i in range(1, M + 1):
        melhor = inf
        for m in moedas:
            if m <= i and dp[i - m] != inf:
                melhor = min(melhor, 1 + dp[i - m])
        dp[i] = melhor

    return dp[M] if dp[M] != inf else Impossible


# ------------------------- Demonstração rápida -------------------------
if __name__ == "__main__":
    exemplos = [
        (6, [1, 3, 4]),        # guloso falha: guloso=3 (4+1+1) vs ótimo=2 (3+3)
        (11, [1, 5, 7]),       # guloso nem sempre ótimo; verifique
        (23, [2, 4, 6]),       # impossível (impar com pares)
        (0, [1, 2, 5]),        # trivial 0
        (100, [1, 5, 10, 25])  # sistema canônico (guloso funciona)
    ]
    funs = [qtdeMoedas, qtdeMoedasRec, qtdeMoedasRecMemo, qtdeMoedasPD]
    for M, moedas in exemplos:
        print(f"M={M}, moedas={moedas}")
        for f in funs:
            try:
                print(f"  {f.__name__}: {f(M, moedas)}")
            except RecursionError:
                print(f"  {f.__name__}: RecursionError (entrada muito grande p/ recursão pura)")
        print("-" * 50)
