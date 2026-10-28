"""
Basic Manim CE Scene Template demonstrating core best practices:
- Grouping with VGroup
- Relative positioning
- LaTeX formulas with raw strings and targeted transforms
- Dynamic ValueTracker with updater
"""

from manim import *


class BestPracticesDemo(Scene):
    def construct(self):
        # 1. Header with relative positioning
        title = Text("Manim Best Practices", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Formula demonstration with raw strings and isolation
        formula_initial = MathTex(
            r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}",
            font_size=48
        )
        formula_initial.set_color_by_tex(r"a^2", YELLOW)
        formula_initial.set_color_by_tex(r"b^2", GREEN)
        formula_initial.set_color_by_tex(r"c^2", RED)

        self.play(FadeIn(formula_initial, shift=DOWN * 0.5))
        self.wait(1)

        # 3. Clean transition using ReplacementTransform
        formula_expanded = MathTex(
            r"{{ c }} = \sqrt{ {{ a^2 }} + {{ b^2 }} }",
            font_size=48
        )
        formula_expanded.set_color_by_tex(r"a^2", YELLOW)
        formula_expanded.set_color_by_tex(r"b^2", GREEN)
        formula_expanded.set_color_by_tex(r"c", RED)

        self.play(ReplacementTransform(formula_initial, formula_expanded))
        self.wait(1)

        # 4. Grouping and repositioning
        calc_group = VGroup(formula_expanded)
        self.play(calc_group.animate.to_edge(LEFT, buff=1.0))

        # 5. Dynamic tracking using ValueTracker and always_redraw
        tracker = ValueTracker(0.0)
        number_label = always_redraw(
            lambda: DecimalNumber(
                tracker.get_value(),
                num_decimal_places=2,
                color=TEAL
            ).next_to(calc_group, RIGHT, buff=1.5)
        )

        self.add(number_label)
        self.play(tracker.animate.set_value(5.0), run_time=2, rate_func=smooth)
        self.wait(1)

        # 6. Smooth conclusion
        self.play(
            FadeOut(title),
            FadeOut(calc_group),
            FadeOut(number_label)
        )
        self.wait(0.5)
