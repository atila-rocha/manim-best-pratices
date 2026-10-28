# Manim Community Edition Syntax Reference

## 1. Mobjects (Mathematical Objects)

### Geometric Mobjects
- `Circle(radius=1.0, color=BLUE)`
- `Square(side_length=2.0, color=GREEN)`
- `Rectangle(width=4.0, height=2.0)`
- `Line(start=LEFT, end=RIGHT)`
- `Arrow(start=LEFT, end=RIGHT, buff=0)`
- `Dot(point=ORIGIN, radius=0.08)`
- `Arc(radius=1.0, angle=PI/2)`
- `Polygon(*vertices)`

### Textual & Mathematical Mobjects
- `Text("Plain text", font_size=36)`: Standard text rendered via Pango.
- `MarkupText("<b>Bold</b> or <i>italic</i>")`: Text with Pango markup formatting.
- `Tex(r"Regular \LaTeX", font_size=42)`: Full LaTeX engine for text and document formatting.
- `MathTex(r"f(x) = \int_0^\infty e^{-t} dt")`: Math-mode LaTeX formula.
- `Typst(r"*Formatted text*")`: Modern Typst-based alternative (when Typst is available).

### Grouping Containers
- `VGroup(*vmobjects)`: Vector group; allows uniform scaling, coloring, arranging, and transforming.
- `Group(*mobjects)`: Generic group containing non-vector or heterogeneous objects.

---

## 2. Positioning & Coordinate System

- `.move_to(target)`: Moves object center to `target` (e.g. `ORIGIN`, coordinate array `[x, y, z]`, or another mobject).
- `.shift(vector)`: Translates object by a relative vector (e.g. `UP * 2 + RIGHT`).
- `.next_to(reference, direction, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)`: Places object adjacent to `reference` along a direction (`UP`, `DOWN`, `LEFT`, `RIGHT`).
- `.align_to(reference, direction)`: Aligns the specified edge/boundary of the object with `reference`.
- `.to_edge(direction, buff=...)`: Aligns with screen boundary (`UP`, `DOWN`, `LEFT`, `RIGHT`).
- `.to_corner(corner, buff=...)`: Aligns with screen corners (`UL`, `UR`, `DL`, `DR`).
- `.arrange(direction=RIGHT, buff=0.25, aligned_edge=ORIGIN)`: Arranges all child elements in a `VGroup`.

---

## 3. Core Animations

### Creation & Entrance
- `Create(vmob)`: Draws vector path progressively.
- `Write(text_or_tex)`: Writes text/equations stroke-by-stroke.
- `FadeIn(mob, shift=UP)`: Fades in with optional positional shift.
- `GrowFromCenter(mob)`: Expands object outward from its center point.
- `DrawBorderThenFill(vmob)`: Outlines vector geometry then fills color.

### Removal & Exit
- `FadeOut(mob, shift=DOWN)`: Fades out object.
- `Uncreate(vmob)`: Undraws vector path in reverse.
- `Unwrite(text_or_tex)`: Erases text backwards.
- `ShrinkToCenter(mob)`: Contracts into center point.

### Transformations & Morphing
- `Transform(mob_a, mob_b)`: Morphs `mob_a` into the shape of `mob_b` (keeps `mob_a` in memory).
- `ReplacementTransform(mob_a, mob_b)`: Morphs `mob_a` into `mob_b` and replaces it in the scene.
- `TransformMatchingTex(source_tex, target_tex)`: Intelligently transforms shared LaTeX substrings.
- `TransformMatchingShapes(source, target)`: Matches similar glyphs and shapes automatically.

### Movement & Indication
- `Rotate(mob, angle=PI/2)`: Rotates object.
- `Indicate(mob, color=YELLOW, scale_factor=1.2)`: Highlights object temporarily.
- `Circumscribe(mob)`: Draws a temporary bounding shape around target.
- `Flash(point)`: Emits radiating lines from a coordinate.
- `Wiggle(mob)`: Shakes object slightly to draw attention.

---

## 4. The `.animate` Syntax

Prepend `.animate` to any modifier method on a Mobject to convert it into a smooth animation inside `self.play()`:
```python
self.play(
    circle.animate.shift(UP * 2).set_fill(RED, opacity=0.8),
    run_time=1.5
)
```

---

## 5. LaTeX Handling & Substring Isolation

- **Always use raw strings**: `MathTex(r"\frac{a}{b}")` (avoids escaping issues).
- **Substring isolation**:
  ```python
  formula = MathTex(
      r"e^{i\pi}", r"+", r"1", r"=", r"0",
      substrings_to_isolate=[r"e^{i\pi}", r"1", r"0"]
  )
  formula.set_color_by_tex(r"e^{i\pi}", BLUE)
  ```
- **Double Brace Syntax**:
  ```python
  formula = MathTex(r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
  # Submobjects can be accessed via index: formula[0], formula[2], etc.
  ```
- **Preamble and Packages**:
  ```python
  template = TexTemplate()
  template.add_to_preamble(r"\usepackage{physics}")
  tex = MathTex(r"\bra{\psi}\ket{\phi}", tex_template=template)
  ```
