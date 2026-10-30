---
name: manim-visual
description: >-
  Linguagem visual para animações de algoritmos e grafos no Manim: paleta de cores unívocas,
  simbologia de legenda (ponto cheio × anel), destacar transições com Flash, layout
  código+grafo+estado em quadrantes, painel de estado estável e checklist de QA visual.
  Carregue junto com manim-best-pratices (fundamentos) e manim-algoritmo (fidelidade).
---

# Manim: Linguagem Visual para Algoritmos

Uma animação didática é lida por cores e símbolos. **Nenhuma cor nem símbolo pode ser ambíguo.**

## 1. Cores unívocas

- Cada **papel/estado** = uma cor exclusiva. Duas cores semelhantes para papéis diferentes (ex.:
  "vértice em análise" × "aresta relaxada") confundem.
- Regra de repetição: a mesma cor sempre significa a mesma coisa na cena inteira.
- Algoritmos precisam de um estado a mais além do convencional (na árvore / explorada): use cor de
  alta distinção, não um tom parecido do conjunto-base. Exemplo validado no projeto:
  - extração da fila: **magenta** `#e879f9` (papel único, não confundível com verde/amarelo);
  - em análise: amarelo; na árvore/MST: `#80ed99` (verde suave); descartada/rejeitada: vermelho apagado.

## 2. Símbolo é uma segunda dimensão (além da cor)

- **Aresta = ponto cheio** na legenda; **vértice = anel/círculo vazio**. Assim o espectador
  distingue *tipo de elemento* pelo símbolo e *estado* pela cor — as duas não se misturam.
- Sempre renderize a legenda na tela ("guia visual") quando as cores do grafo mudam.

## 3. Destacar transições (Flash / indicador)

- `Flash` em extração/decisão: use `line_length` e `stroke_width` controlados e **flash maior** que
  o padrão para não passar despercebido; a cor deve espelhar o estado (ex.: magenta na extração).
- O indicador de linha do `CodePanel` nasce na posição `encaixar()` da **primeira linha executada**
  e desliza com os passos — nunca nasce "pulando" para o meio do bloco.
- Estado "verificado mas sem efeito" não deve parecer uma transição: mantenha-o como cor de análise,
  não pinte como se algo tivesse mudado.

## 4. Layout em quadrantes para execução de algoritmo

```
+--------------------------------------------------------------+
| Cabeçalho / título            (y ∈ [3.0, 3.6])                |
+-----------------------------+--------------------------------+
| Código (CodePanel, 0.5×0.55) | Grafo / visualização           |
| Legenda abaixo do código     | Painel de estado (dir. inf.)   |
|   (x ∈ [-6.6, -0.4])        |   (x ∈ [0.4, 6.6])            |
+-----------------------------+--------------------------------+
```

- Gutter central: `x ∈ [-0.4, 0.4]` sempre livre.
- Clearance: nós do grafo ≥ 0,5 unidades acima do topo do painel de estado.

## 5. Painel de estado estável (sem trepidação)

- Alinhamento à esquerda (`aligned_edge=LEFT` ancorado no card) — textos centralizados trepidam
  quando o número de dígitos muda.
- Dimensione o card pelo **pior caso** da string (ex.: "MST Concluída! 5 arestas (|V|-1) selecionadas").

## 6. Checklist de QA visual (antes de renderizar 1080p)

| # | Item | Critério |
|---|------|----------|
| 1 | Guia visual sem cores ambíguas | Nenhum par de papéis usa tons que se confundem |
| 2 | Legenda completa | Toda cor/símbolo ativo aparece na legenda |
| 3 | Extração ≠ relaxamento | A extração (flash magenta) é distinguível da aresta relaxada |
| 4 | Bounds | Nada fora de `x ∈ [-6.6, 6.6]`, `y ∈ [-3.6, 3.6]` |
| 5 | Frame estático | Provar frames críticos com `manim -s` e conferir visualmente |
| 6 | Daltonismo | Estados nunca separados só por vermelho/verde |
