# Guia de Layout, Espaçamento e Isolamento Visual no Manim CE

Este guia estabelece os padrões e boas práticas para estruturar layouts limpos, legíveis e sem sobreposição de elementos em animações educacionais e técnicas com o **Manim Community Edition**.

---

## 1. Sistema de Coordenadas e Orçamento Espacial (Canvas Budgeting)

No Manim (proporção padrão 16:9), as dimensões da câmera padrão são:
- **Largura total**: `config.frame_width = 14.22` unidades ($x \in [-7.11, +7.11]$)
- **Altura total**: `config.frame_height = 8.0` unidades ($y \in [-4.0, +4.0]$)
- **Área Segura (Safe Frame Margin)**: $x \in [-6.6, +6.6]$, $y \in [-3.6, +3.6]$. Deixe sempre pelo menos $0.4 \sim 0.5$ unidades de respiro em relação às bordas externas do vídeo.

### Regra de Ouro do Orçamento Espacial
Antes de posicionar elementos na cena, defina a partição matemática das regiões da tela. **Nenhum elemento deve invadir a região designada para outro.**

```
+-------------------------------------------------------------------------+
|                  CABEÇALHO / TÍTULO (y in [3.0, 3.6])                   |
+------------------------------------+------------------------------------+
|                                    |                                    |
|         COLUNA ESQUERDA            |          COLUNA DIREITA            |
|       (x in [-6.6, -0.4])          |         (x in [0.4, 6.6])          |
|                                    |                                    |
|  - Painel de Código / Conceitos    |  - Grafo / Diagrama / Visualização |
|  - Legendas Didáticas              |  - Dashboard / Painel de Status    |
|                                    |                                    |
+------------------------------------+------------------------------------+
```

---

## 2. Padrões Canônicos de Layout

### A. Divisão em 2 Colunas (Split-Screen)
Ideal para comparar código com visualização ou apresentar conceitos teóricos ao lado de um exemplo prático.
- **Coluna Esquerda**: Centro em $x \approx -3.5$, largura máxima de $6.0 \sim 6.2$ unidades.
- **Coluna Direita**: Centro em $x \approx +3.5$, largura máxima de $6.0 \sim 6.2$ unidades.
- **Gutter Central (Respiro)**: Mínimo de $0.6 \sim 0.8$ unidades livre no eixo X ($x \in [-0.4, +0.4]$).

### B. Grade de 4 Quadrantes (Code + Legend + Graph + Dashboard)
Usada com grande eficácia em algoritmos iterativos (ex: Kruskal, Dijkstra):
1. **Cabeçalho Superior**: $y \in [3.0, 3.6]$ (`to_edge(UP, buff=0.35)`).
2. **Superior Esquerdo**: Bloco de código com escala reduzida (`scale(0.50)` a `0.55`).
3. **Inferior Esquerdo**: Guia visual ou legenda de cores alinhada abaixo do código (`next_to(code, DOWN, buff=0.4, aligned_edge=LEFT)`).
4. **Superior Direito**: Grafo ou visualização gráfica posicionada no quadrante positivo de Y ($y \in [-0.5, 2.5]$).
5. **Inferior Direito**: Painel de estado/dashboard posicionado em $y \in [-3.5, -1.2]$.

---

## 3. Container-First: Painéis Backdrop como Limites Físicos

A causa primária de sobreposições visuais é renderizar elementos "soltos" no espaço sem um delimitador visual pré-estabelecido.

### Prática Recomendada:
1. Crie um contêiner `RoundedRectangle` com dimensões explícitas e fundo opaco/translúcido (`fill_color=..., fill_opacity=0.85-0.95`).
2. Centralize ou alinhe os textos e subelementos **relativamente ao contêiner**:
   ```python
   painel = RoundedRectangle(
       corner_radius=0.15,
       width=6.2,
       height=5.2,
       color=GRAY_D,
       stroke_width=1.5,
       fill_color="#151824",
       fill_opacity=0.9
   ).move_to(np.array([-3.5, -0.65, 0]))

   # Alinhar grupo de conteúdo internamente ao centro do painel
   lista_itens.move_to(painel.get_center())
   ```

### Vantagens do Container-First:
- **Barreira Visual Concreta**: O espectador identifica claramente onde termina a explicação e onde começa a demonstração.
- **Prevenção de Deriva (Drift)**: Modificações de texto durante a animação não vazam porque o contêiner serve de âncora fixa.

---

## 4. Prevenção de Estouro de Texto (Text Overflow)

Frases longas em uma única linha são a principal razão de quebra de layout no Manim, pois o `Text` e o `MathTex` **não quebram linha automaticamente**.

### Regras para Textos e Fórmulas:
1. **Nunca use frases longas em uma única string horizontal**:
   ```python
   # INCORRETO: Ultrapassa a tela e invade outros elementos
   Text("• Conectividade: Conecta todos os |V| vértices em uma única componente conexa", font_size=20)

   # CORRETO: Quebre em título em negrito + subtítulo descritivo identado
   tit = Text("• Conectividade Total:", font_size=16, color=WHITE, weight=BOLD)
   desc = Text("  Conecta todos os |V| vértices em 1 componente", font_size=14, color=GRAY_A)
   item = VGroup(tit, desc).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
   ```

2. **Hierarquia Tipográfica Recomendada para Telas Divididas**:
   - **Título Principal da Cena**: `font_size=26` a `32`
   - **Subtítulo / Header**: `font_size=18` a `20`
   - **Títulos de Seção / Cards**: `font_size=15` a `17` (com `weight=BOLD`)
   - **Texto de Itens / Explicações**: `font_size=13` a `15`
   - **Badges / Detalhes / Legendas**: `font_size=12` a `14`
   - **Blocos de Código (`Code`)**: `.scale(0.50)` a `.scale(0.55)`

3. **Restrição de Largura Máxima**:
   - Em layout de 2 colunas, nenhum grupo de texto deve exceder `width = 5.6`.
   - Se um texto ultrapassar a largura do painel menos o padding (`card.width - 0.6`), reduza a fonte ou quebre em mais linhas usando `arrange(DOWN, aligned_edge=LEFT)`.

---

## 5. Isolamento Geométrico de Grafos e Diagramas

Em diagramas e grafos interativos:
1. **Verificação de Coordenadas Extremas**:
   - Calcule as coordenadas mínimas e máximas dos nós:
     $$\min(y_{\text{nós}}) - \text{raio}_{\text{nó}} > y_{\text{topo\_painel\_inferior}} + \text{respiro}$$
   - Se o painel inferior começa em $y = -1.20$, os nós mais baixos do grafo devem estar posicionados em no mínimo $y \ge -0.30$, garantindo pelo menos $0.6$ unidades de folga livre.

2. **Posicionamento de Rótulos de Arestas**:
   - Não use offsets arbitrários ou fixos que possam sobrepor arestas adjacentes.
   - Calcule o vetor normal unitário à aresta:
     ```python
     dir_normal = np.array([-(p2[1]-p1[1]), p2[0]-p1[0], 0])
     dir_normal = dir_normal / np.linalg.norm(dir_normal)
     pos_label = mid + 0.18 * dir_normal
     ```
   - Em caso de arestas quase horizontais ou verticais, aplique um ajuste explícito (`UP * 0.20` ou `RIGHT * 0.20`) para evitar cruzamentos com nós vizinhos.

---

## 6. Atualizações Dinâmicas de Estado sem Trepidação

Ao atualizar painéis de status (ex: contadores de arestas, peso total, estado do Union-Find):
1. **Âncoras de Alinhamento**:
   - Evite substituir textos centralizados se as strings tiverem tamanhos muito diferentes; isso faz o texto trepidar horizontalmente.
   - Use `aligned_edge=LEFT` no `VGroup` e alinhe à esquerda do painel (`card.get_left() + RIGHT * 0.4`).
2. **Dimensionamento pelo Pior Caso**:
   - Dimensione o painel considerando o texto mais longo da execução (ex: "MST Concluída! 5 arestas (|V|-1) selecionadas").

---

## 7. Checklist de Validação de Layout (QA de Telas)

Antes de aprovar e renderizar vídeos finais em alta resolução (`-pqh`):

| # | Item de Verificação | Critério de Aceite |
|---|---------------------|--------------------|
| 1 | **Margem de Borda Externa** | Todos os objetos estão dentro de $x \in [-6.6, 6.6]$ e $y \in [-3.6, 3.6]$? |
| 2 | **Isolamento de Quadrantes** | A coluna da esquerda nunca cruza para $x > -0.3$? O diagrama nunca ultrapassa $x < +0.3$? |
| 3 | **Clearance Vertical** | A base do diagrama possui folga $\ge 0.5$ unidades em relação ao topo do dashboard inferior? |
| 4 | **Sem Frases Longas Contínuas** | Textos explicativos estão quebrados em título + descrição e contidos dentro do card? |
| 5 | **Escala de Código Legível** | Blocos `Code` estão com scale entre `0.48` e `0.55` com espaçamento para legendas abaixo? |
| 6 | **Inspeção de Frame Estático** | O comando `manim -s -pql arquivo.py Cena` foi executado nos frames críticos para conferir bounds? |
