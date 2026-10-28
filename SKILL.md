---
name: manim-best-practices
description: >-
  Provides best practices, non-obvious patterns, syntax guidance, and performance optimization for creating high-quality mathematical animations with Manim Community Edition (ManimCE). Activate this skill whenever the user asks to write, debug, refactor, optimize, or design Manim animation scripts, scenes, mobjects, or video assets.
---

# Manim Best Practices

This skill provides expert guidance for designing and implementing mathematically precise, visually compelling, and performant animations using the **Manim Community Edition (ManimCE)**.

## Core Principles

- **Programmatic Precision**: Define spatial coordinates, relative offsets, and timing curves deterministically using Python code rather than guessing values.
- **Composition over Complexity**: Encapsulate related visual elements into `VGroup` containers to apply unified transformations, alignments, and scalings.
- **Spatial Budgeting & Isolation**: Explicitly partition screen real estate (`frame_width=14.22`, `frame_height=8.0`). Delimit text and diagrams with backdrop cards (`RoundedRectangle`) and never let elements encroach on adjacent quadrants.
- **Visual Clarity & Continuity**: Prefer `ReplacementTransform` or `TransformMatchingTex` over standard `Transform` to prevent ghost objects and overlapping geometries. Use `.animate` for fluid property transitions.
- **Iterative Drafting**: Always test animations in low quality (`-pql`) first to maintain high development velocity before final high-resolution rendering (`-pqh`).

## Essential Workflow

1. **Scene Structure**:
   - Subclass `Scene` (or specialized scenes like `MovingCameraScene`, `ThreeDScene`).
   - Implement all animation sequencing inside the `construct(self)` method.

2. **Mobject Lifecycle**:
   - **Instantiate**: Create Mobjects (`Circle`, `Square`, `Text`, `MathTex`).
   - **Configure**: Set properties (`color`, `fill_opacity`, `stroke_width`) before adding to scene.
   - **Position**: Arrange relative to other elements using `next_to`, `shift`, `move_to`, or `align_to`.
   - **Animate**: Play transitions with `self.play(...)` and control pacing with `self.wait(...)`.

3. **Key Layout Patterns**:
   - **Spatial Partitions**: Split screens into left (`x in [-6.6, -0.4]`) and right (`x in [0.4, 6.6]`) with central gutter.
   - **Container-First Cards**: Use `RoundedRectangle` as a physical container; position text strictly relative to `card.get_center()` or `card.get_left()`.
   - **Text Overflow Prevention**: Split explanations into structured items with a bold title and indented subtitle (`VGroup(t, d).arrange(DOWN, aligned_edge=LEFT)`). Never use long single-line strings.
   - **Diagram Clearance**: Maintain at least $0.5$ units clearance between graph nodes and bottom panels/headers.
   - **Relative Positioning**: `obj_b.next_to(obj_a, RIGHT, buff=0.3)`
   - **Group Alignment**: `VGroup(m1, m2, m3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)`
   - **Screen Anchors**: `obj.to_edge(UP)` or `obj.to_corner(UL)`

4. **Mathematical Typography & Raw Strings**:
   - Always use raw strings (`r"..."`) for LaTeX to prevent escape sequence errors.
   - Use `MathTex` for formulas and `Text` (or `MarkupText`) for textual descriptions.
   - Isolate parts of formulas with `substrings_to_isolate` or `{{ ... }}` for targeted animations or color accents.

5. **Dynamic Updates**:
   - Use `ValueTracker` paired with `.add_updater()` or `always_redraw(...)` for continuous variables, graphs, or counters.

## Detailed References & Examples

- **[Layout & Spacing Guidelines](references/layout_guidelines.md)**: Deep dive into 16:9 canvas budgeting, multi-panel grids, text wrapping, and layout QA checklist.
- **[Syntax Reference](references/syntax.md)**: Comprehensive catalog of Mobjects, animations, transforms, and LaTeX methods.
- **[Best Practices Guide](references/best_practices.md)**: Visual pacing, color harmony, performance tips, and coding standards.
- **[Split Screen Layout Example](examples/split_screen_layout.py)**: Runnable template demonstrating non-overlapping panels, cards, and state dashboards.
- **[Basic Example Scene](examples/basic_scene.py)**: Runnable example showing composition, LaTeX transformations, and updaters.
