
# DYNAMIC PROGRAMMING 2025/2 — Checkpoint: O Desafio das Moedas

**Disciplina:** Dynamic Programming — **Professor:** Marcelo Amorim

## 👥 Integrantes (RA e Nome Completo)
- Arthur Galvão Alves — **RM554462**
- Henrique Ignacio Bartalo — **555274**
- Gustavo Henrique Martins — **RM556956**

---

## 1) Introdução e Contextualização

**Problema (Coin Change):** dado um montante inteiro **M ≥ 0** e um conjunto de moedas **moedas** com disponibilidade ilimitada, deseja-se **minimizar** o número de moedas cuja soma seja exatamente **M**. Se for impossível, indicamos impossibilidade (usamos **-1**).

**Por que é um Problema de Otimização?** buscamos o **melhor** (mínimo) entre todas as combinações viáveis. A solução ótima global decorre da combinação ótima de subsoluções.

**Programação Dinâmica (PD):**
- **Subestrutura Ótima:** o ótimo de **M** depende dos ótimos de submontantes `M - m` para cada moeda `m`.
- **Subproblemas Sobrepostos:** vários submontantes são reavaliados muitas vezes nas abordagens ingênuas, tornando **memoização**/**PD** poderosas.

---

## 2) Análise das Abordagens e Complexidades

Implementamos quatro funções no arquivo `coin_change.py`:

### (1) Estratégia Gulosa — `qtdeMoedas(M, moedas)`
- **Ideia:** ordenar moedas em ordem decrescente e sempre pegar a maior possível até completar M.
- **Limitação:** não é ótima para sistemas arbitrários de moedas.  
  **Exemplo:** `M=6, moedas=[1,3,4]`  
  Guloso devolve **3** (4+1+1), mas o ótimo é **2** (3+3).
- **Complexidade:** tempo `O(k log k + a)` (k=tipos de moedas; a=moedas usadas), espaço `O(k)` pela ordenação.

### (2) Recursiva Pura — `qtdeMoedasRec(M, moedas)`
- **Ideia:** definir `f(M) = min(1 + f(M-m))` sobre todas `m ≤ M`, com `f(0)=0`.
- **Árvore de Recursão:** para `M=6` e `[1,3,4]`, os nós para `f(6)` ramificam em `f(5)`, `f(3)`, `f(2)`, etc., e subproblemas como `f(2)` e `f(3)` reaparecem muitas vezes.
- **Custo:** tempo **exponencial** (~`O(k^M)`), espaço `O(M)` de pilha. Adequada só para M pequeno.

### (3) Recursiva com Memoização (Top-Down) — `qtdeMoedasRecMemo(M, moedas)`
- **Ideia:** cachear resultados de `f(x)`; cada submontante é resolvido uma única vez.
- **Relação com PD:** é PD **Top-Down** (recursão + cache).
- **Custo:** tempo `O(k*M)`, espaço `O(M)`.

### (4) PD Bottom-Up — `qtdeMoedasPD(M, moedas)`
- **Ideia:** vetor `dp` onde `dp[i]` guarda a menor quantidade de moedas para formar `i`.  
  Transição: `dp[i] = min(1 + dp[i-m])` para moedas `m ≤ i`, com `dp[0]=0`.
- **Vantagem:** evita overhead de chamadas recursivas e tende a ser levemente mais rápida.
- **Custo:** tempo `O(k*M)`, espaço `O(M)`.

---

## 3) Conclusão

| Abordagem | Tempo (pior caso) | Espaço |
|---|---|---|
| Gulosa | `O(k log k + a)` | `O(k)` |
| Recursiva pura | ~`O(k^M)` | `O(M)` |
| Recursiva + Memo (Top-Down) | `O(k*M)` | `O(M)` |
| PD Bottom-Up | `O(k*M)` | `O(M)` |

**Escolha recomendada:** `qtdeMoedasPD` (Bottom-Up) ou `qtdeMoedasRecMemo` (Top-Down) pela robustez e custo `O(k*M)`. A gulosa é rápida mas não garante ótimo geral; a recursiva pura explode para M grandes.

---

## 📦 Como executar (exemplos)

```bash
python3 cp5_dynamic.py
```

Saída ilustrativa (parcial):

```
M=6, moedas=[1, 3, 4]
  qtdeMoedas: 3
  qtdeMoedasRec: 2
  qtdeMoedasRecMemo: 2
  qtdeMoedasPD: 2
```

> Observa-se o fracasso do guloso neste caso, enquanto as abordagens com PD encontram o ótimo.
