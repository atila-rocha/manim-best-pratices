---
name: manim-algoritmo
description: >-
  Como animar um algoritmo (grafo, ordenação, busca) com fidelidade usando Manim: dissecar a
  implementação, gravar a execução real em passos (recorder/trace), modo linha a linha didático,
  ritmo de pausa, testes dourados e comparação por índice de passo (nunca por timestamp).
  Carregue junto com manim-best-pratices (fundamentos) e manim-pipeline (render).
---

# Manim: Animando Algoritmos com Fidelidade

O objetivo didático é mostrar o **algoritmo real**, não uma versão recriada. Todo estado exibido
na tela deve sair de uma execução verdadeira da implementação. Nunca fabrique estados à mão.

## 1. Princípios

1. **Não reimplementar no roteiro**: instrumente a implementação real (ex.: `algs4-py` do projeto)
   com hooks que disparam a cada evento relevante. A cena Manim só consome a sequência de eventos.
2. **Um passo por evento de trace**: cada evento de execução vira um `Step` imutável
   (`evento`, `linha`, quantidade de iteração, trecho de código, `pausa`).
3. **Estado vem do evento seguinte**: o trace avisa a *linha*, depois executa a linha e grava o
   estado. Portanto, o estado visual de um passo é o estado pós-evento; use o state do evento
   seguinte como dado de entrada para não desenhar uma transição antecipada.
4. **Fontes de verdade internas**: leia o estado de estruturas reais do algoritmo (ex.: a heap em
   `pq.pq` do IndexMinPQ) em vez de refazer a derivação na mão. Grave `contains` exatamente como
   o algoritmo se comporta, mesmo que semanticamente pareça redundante.
5. **Filtros de eventos**: remova eventos que gerariam passos duplicados (ex.: um bloco repetido
   no Eager) para não quebrar o didatismo; documente o filtro no código.
6. **Grafo canônico único por projeto**: defina uma única instância (ex.: 6 nós, 8 arestas, custo
   13: `1-2(1), 0-1(2), 3-4(2), 2-4(3), 0-2(4), 3-5(5), 4-5(6), 1-3(7)`) para todos os vídeos e
   para os testes dourados. Algoritmos sem raiz (Kruskal) começam pela menor aresta, não no vértice 0.

## 2. Dois modos de coleta no mesmo gravador

| Modo | Granularidade | Uso |
|---|---|---|
| `coletar()` compacto | 1 passo por iteração/etapa | **golden test** de estados e determinismo |
| `coletar_detalhado()` linha a linha | 1 passo por evento de trace | material didático; o vídeo segue o código passo a passo |

Regras para os dois modos:
- A projeção visual (método `aplicar(state)`) é **compartilhada**: o que muda é só a lista de passos.
  Isso garante que o final detalhado termina exatamente no estado do compacto.
- Descritores por linha: cada evento precisa saber dizer "o que está acontecendo" em uma frase curta
  (ex.: *lê a aresta de menor peso da fila*), usada na legenda do vídeo.

## 3. Ritmo (Step.pausa)

- **Decisão** (aresta aceita/rejeitada, extração da fila, retorno): `pausa ≈ 1,7 s` — o espectador
  precisa absorver o porquê.
- **Bookkeeping** (varredura, atualização de heap, incremento de índice): `pausa ≈ 0,55 s`.
- Animação por passo: `≈ 0,45 s` de FadeIn/Transform em cima da pausa.
- O vídeo pode ser longo; o modo linha a linha é **sequencial** de propósito.

## 4. Testes dourados (validator)

Antes de renderizar, um script de validação deve conferir, por índice de passo:
- recorte de código: toda linha de código exibida existe no arquivo-fonte real;
- linhas obrigatórias presentes (início/laço/fim do algoritmo);
- estado final do modo detalhado **idêntico** ao do modo compacto;
- monotonicidade (contadores/peso só crescem ou estabilizam, nunca regridem);
- pausas dentro de limites (não negativas, não absurdas).
- Exporte um `stages.json` (índice de passos) para comparar revisões **por índice**, nunca por
  timestamp — a duração do vídeo muda entre takes e não é um bom comparador.

## 5. Componentes da cena

- `CodePanel`: mostra o trecho de código real e um **indicador de linha atual** que nasce na
  `encaixar()`-posição da primeira linha executada (não no meio do bloco) e desliza conforme avança.
- `GraphView`: vértices/arestas; cores por estado (ver `manim-visual`).
- `StatePanel`: contadores e estado das estruturas (fila, UF, peso) com alinhamento à esquerda.
- Cena base que itera `for passo in passos: aplicar(passo); pausa(passo.pausa)` e centraliza toda a
  contabilidade em `Step` — nada de `wait(1)` arbitrário.

## 6. Referências práticas no projeto

- `mst_record.py`: gravador + `Step` + roteiros por linha (Kruskal/Lazy/Eager).
- `mst_common.py`: `CodePanel`, `GraphView`, `StatePanel`, cena base.
- `validate_mst_scenes.py`: os 5 testes dourados + exportação de `stages.json`.
