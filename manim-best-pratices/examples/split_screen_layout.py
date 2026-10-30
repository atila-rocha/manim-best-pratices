"""
Template de Layout de 2 Colunas e Painéis com Isolamento Visual no Manim CE.
Demonstra as práticas recomendadas em `references/layout_guidelines.md`:
- Orçamento espacial (Canvas Budgeting: Split-Screen)
- Padrão Container-First (RoundedRectangle como barreira de layout)
- Hierarquia tipográfica e quebra de linhas em VGroup
- Isolamento vertical entre diagrama superior e dashboard inferior
"""

from manim import *
import numpy as np


class SplitScreenTemplateScene(Scene):
    def construct(self):
        # 0. Cores temáticas consistentes
        COLOR_BG = "#0f111a"
        COLOR_PANEL = "#151824"
        COLOR_ACCENT = "#48cae4"
        COLOR_OK = "#06d6a0"
        self.camera.background_color = COLOR_BG

        # 1. Cabeçalho Superior (Isolado no topo: y in [2.8, 3.6])
        titulo = Text("Estrutura de Layout Dividido (Split-Screen)", font_size=28, color=WHITE, weight=BOLD)
        subtitulo = Text("Padrão de isolamento entre teoria, diagrama e dashboard", font_size=16, color=COLOR_ACCENT)
        cabecalho = VGroup(titulo, subtitulo).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)

        self.play(FadeIn(cabecalho, shift=DOWN * 0.3))

        # 2. Painel Esquerdo (Teoria / Código / Conceitos: x in [-6.6, -0.4])
        painel_esq = RoundedRectangle(
            corner_radius=0.15,
            width=6.2,
            height=5.2,
            color=GRAY_D,
            stroke_width=1.5,
            fill_color=COLOR_PANEL,
            fill_opacity=0.9
        ).move_to(np.array([-3.5, -0.65, 0]))

        tit_secao = Text("Conceitos & Regras:", font_size=17, color=COLOR_ACCENT, weight=BOLD)

        # Itens com título + descrição (evita overflow horizontal)
        i1_t = Text("• Orçamento Espacial:", font_size=15, color=WHITE, weight=BOLD)
        i1_d = Text("  Delimita regiões e impede invasões de tela", font_size=13, color=GRAY_A)
        item_1 = VGroup(i1_t, i1_d).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

        i2_t = Text("• Container-First:", font_size=15, color=WHITE, weight=BOLD)
        i2_d = Text("  Painéis delimitam áreas físicas visíveis", font_size=13, color=GRAY_A)
        item_2 = VGroup(i2_t, i2_d).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

        i3_t = Text("• Tipografia Hierárquica:", font_size=15, color=COLOR_OK, weight=BOLD)
        i3_d = Text("  Fontes de 13pt a 16pt para telas divididas", font_size=13, color=GRAY_A)
        item_3 = VGroup(i3_t, i3_d).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

        conteudo_esq = VGroup(tit_secao, item_1, item_2, item_3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        ).move_to(painel_esq.get_center())

        self.play(FadeIn(painel_esq), FadeIn(conteudo_esq))

        # 3. Painel Direito Superior: Diagrama / Grafo (y in [-0.5, 2.3], x in [0.5, 6.5])
        coords = {
            "A": np.array([1.8, 1.6, 0]),
            "B": np.array([5.2, 1.6, 0]),
            "C": np.array([5.2, -0.2, 0]),
            "D": np.array([1.8, -0.2, 0]),
        }

        nos = {}
        for k, pos in coords.items():
            circ = Circle(radius=0.28, color=GRAY_C, fill_color="#2b2d42", fill_opacity=1.0).move_to(pos)
            txt = Text(k, font_size=15, color=WHITE).move_to(pos)
            nos[k] = VGroup(circ, txt)

        linhas = [
            Line(coords["A"], coords["B"], color=GRAY, stroke_width=3),
            Line(coords["B"], coords["C"], color=GRAY, stroke_width=3),
            Line(coords["C"], coords["D"], color=GRAY, stroke_width=3),
            Line(coords["D"], coords["A"], color=GRAY, stroke_width=3),
        ]
        diagrama = VGroup(*linhas, *nos.values())
        self.play(Create(diagrama), run_time=1.0)

        # 4. Painel Direito Inferior: Dashboard de Estado (y in [-3.5, -1.2], x in [0.4, 6.6])
        painel_dash = RoundedRectangle(
            corner_radius=0.15,
            width=6.2,
            height=1.8,
            color=GRAY_D,
            stroke_width=1.5,
            fill_color=COLOR_PANEL,
            fill_opacity=0.9
        ).move_to(np.array([3.5, -2.35, 0]))

        st_tit = Text("Painel de Estado (Dashboard):", font_size=15, color=COLOR_ACCENT, weight=BOLD)
        st_info = Text("Estado: Diagrama isolado com 0.65u de respiro", font_size=13, color=WHITE)
        st_metrica = Text("Status: Sem colisões ou estouro de texto", font_size=13, color=COLOR_OK)

        dash_conteudo = VGroup(st_tit, st_info, st_metrica).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12
        ).move_to(painel_dash.get_center())

        self.play(FadeIn(painel_dash), FadeIn(dash_conteudo))
        self.wait(2.0)
