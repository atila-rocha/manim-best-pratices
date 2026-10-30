# Manim Best Practices & Optimization Guide

## 1. Visual Quality & Direction

- **Pacing**:
  - Always allow pauses after key reveals (`self.wait(1)` to `self.wait(2)`).
  - Use brief pauses (`self.wait(0.5)`) between consecutive minor transformations so the viewer can follow transitions comfortably.
  - Adjust `run_time` based on complexity: simple shifts need `0.5s - 1.0s`, while intricate multi-part transformations need `1.5s - 3.0s`.

- **Color Palettes**:
  - Use coherent, muted base colors with high-contrast accent colors (e.g. `BLUE`, `TEAL`, `YELLOW`, `RED`).
  - Avoid using pure white on black for everything; soften with `GREY_A`, `GREY_B`, or pastels.
  - Maintain color semantics across the scene (e.g., if velocity is represented in `GREEN`, keep all velocity indicators `GREEN`).

- **Morphing Hygiene**:
  - Always prefer `ReplacementTransform` over `Transform` when the source object is no longer needed. This prevents invisible ghost objects from lingering in the scene and causing rendering artifacts or layout conflicts.

- **Layout Architecture & Space Isolation**:
  - **Screen Bounds**: Always respect default 16:9 bounds (`x in [-7.11, +7.11]`, `y in [-4.0, +4.0]`). Keep content within safe limits (`[-6.6, +6.6]`, `[-3.6, +3.6]`).
  - **Container-First Pattern**: Use `RoundedRectangle` backdrop cards with explicit widths and heights as physical boundaries for text and data panels.
  - **Text Overflow Prevention**: Never write long unformatted horizontal text strings. Break explanations into structured items with a bold title and indented description using `VGroup(tit, desc).arrange(DOWN, aligned_edge=LEFT)`.
  - **Diagram Clearance**: Ensure coordinates of graph nodes and geometric shapes have at least `0.5` units clearance from adjacent text boxes or dashboards.
  - *Detailed guide*: See [Layout Guidelines](layout_guidelines.md).

- **Dynamic Reactive Elements**:
  - For values that change continuously over time, use `ValueTracker` along with `always_redraw(...)` or `.add_updater(...)`:
    ```python
    t = ValueTracker(0)
    dot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), np.sin(t.get_value()))))
    self.add(dot)
    self.play(t.animate.set_value(TAU), run_time=4, rate_func=linear)
    ```

---

## 2. Technical Performance & Optimization

- **Render Resolution Flags**:
  - **Iterative Drafting**: `manim -pql scene.py SceneName` (480p, 15fps, fast render + instant preview).
  - **Medium Quality**: `manim -pqm scene.py SceneName` (720p, 30fps).
  - **High Quality (Production)**: `manim -pqh scene.py SceneName` (1080p, 60fps).
  - **4K Ultra**: `manim -pqk scene.py SceneName` (2160p, 60fps).
  - **Last Frame Only**: `manim -s -pqh scene.py SceneName` (outputs a static PNG image).

- **Parallel Animation Execution**:
  - Group independent animations inside a single `self.play(...)` call rather than separate calls to keep motion synchronous:
    ```python
    self.play(
        Create(axes),
        Write(title),
        run_time=1.5
    )
    ```

- **Avoid Redundant Re-creation**:
  - Instead of uncreating and creating new mobjects for minor text or property changes, use `.animate` or `TransformMatchingTex`.

---

## 3. Code Standards & Architecture

- **Descriptive Naming**: Name Mobjects by their semantic role (e.g., `pythagoras_eq`, `hypotenuse_brace`, `input_vector`) instead of generic numbered names like `t1`, `t2`.
- **Hierarchical VGroups**:
  - Group subcomponents logically: `diagram = VGroup(axes, curve, tangent_line, label)`.
  - Moving or scaling `diagram` automatically preserves relative distances and alignments.
- **Scene Modularity**:
  - Divide long scenes into distinct helper methods within the `Scene` class (`setup_axes()`, `animate_proof()`, `conclude()`) to maintain clean, readable code.
