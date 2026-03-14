# Text & LaTeX in ManimGL

Source files: `manimlib/mobject/svg_mobject/tex_mobject.py`, `manimlib/mobject/svg_mobject/string_mobject.py`

---

## Class Selection

| Class | Use for | Backend |
|-------|---------|---------|
| `Tex` | LaTeX math expressions | LaTeX → SVG |
| `TexText` | Mix of text and math (`Hello $x^2$`) | LaTeX → SVG |
| `Text` | Plain text, no LaTeX needed | Pango |
| `MarkupText` | Text with Pango markup (`<b>bold</b>`) | Pango |

**`MathTex` does not exist in ManimGL.** Always use `Tex` for math.

---

## Basic Usage

```python
# Math expression
eq = Tex(r"\frac{d}{dx} \sin(x) = \cos(x)")

# Mixed text and math
label = TexText(r"The derivative of $\sin(x)$ is $\cos(x)$")

# Plain text
title = Text("Unit Circle")

# Pango markup
bold = MarkupText("<b>important</b> and <i>italic</i>")
```

---

## LaTeX Pipeline

1. ManimGL writes a `.tex` file using your string + a template from `tex_templates.yml`
2. MacTeX compiles `.tex` → `.dvi`
3. `dvisvgm` converts to SVG
4. SVG is parsed into Bezier paths → `VMobject`

This means LaTeX compile errors appear in the terminal, not as Python exceptions.

---

## Sizing & Positioning

```python
eq = Tex(r"f(x) = \sin(x)")

# Scaling
eq.scale(1.4)                        # make bigger
eq.scale(0.6)                        # make smaller

# Positioning
eq.to_edge(UP)                       # snap to top edge with default buffer
eq.to_edge(UP, buff=0.3)             # custom buffer
eq.to_corner(UL)                     # upper-left corner
eq.move_to(ORIGIN)                   # center of screen
eq.shift(DOWN * 0.5)                 # relative move
eq.next_to(other_mob, DOWN, buff=0.2)  # position relative to another object
eq.align_to(other_mob, LEFT)         # align left edges

# Center on specific axis only
eq.move_to(np.array([0, 2, 0]))      # set explicit position
```

---

## Color

```python
# Whole object
eq = Tex(r"\sin(\theta)", color=YELLOW)
eq.set_color(RED)

# By submobject index (each character/glyph is a submobject)
eq[0].set_color(BLUE)

# Gradient
eq.set_color_by_gradient(BLUE, RED)

# Highlight a substring — use get_part_by_tex
eq = Tex(r"\sin(\theta) = \frac{\text{opp}}{\text{hyp}}")
eq.get_part_by_tex(r"\sin").set_color(YELLOW)
```

---

## Grouping Multiple Expressions

```python
# VGroup — position and animate together
labels = VGroup(
    Tex(r"\sin\theta"),
    Tex(r"= \frac{\text{opp}}{\text{hyp}}"),
)
labels.arrange(RIGHT, buff=0.2)      # lay out horizontally
labels.arrange(DOWN, buff=0.4)       # or vertically

# Access individual items
labels[0].set_color(RED)
```

---

## Animating Text

```python
# Draw text stroke-by-stroke (use for LaTeX/math)
self.play(Write(eq))

# Draw shape outline then fill (good for geometric text)
self.play(DrawBorderThenFill(eq))

# Simple fade
self.play(FadeIn(eq))
self.play(FadeOut(eq))

# Animate a property change
self.play(eq.animate.scale(0.6).to_edge(UP))

# Transform one expression into another (morphs glyphs)
eq2 = Tex(r"f'(x) = \cos(x)")
self.play(Transform(eq, eq2))

# Transform and replace (eq is removed, eq2 takes over)
self.play(ReplacementTransform(eq, eq2))
```

---

## TransformMatchingTex

Morphs matching substrings between two `Tex` objects — great for showing equation manipulations:

```python
eq1 = Tex(r"x^2 + 2x + 1")
eq2 = Tex(r"(x + 1)^2")
self.play(TransformMatchingTex(eq1, eq2))
```

Matching is based on the LaTeX source string of each glyph group. Non-matching parts fade in/out.

---

## Updating Text Position (with updaters)

```python
label = Tex(r"\theta", color=YELLOW)
label.add_updater(lambda m: m.next_to(some_mob, UP, buff=0.1))

# Or position by a computed point
label.add_updater(lambda m: m.move_to(
    circle_center + 0.7 * np.array([np.cos(t / 2), np.sin(t / 2), 0])
))
```

---

## Pi / Axis Labels Pattern

Common pattern for labeling axis tick marks:

```python
pi_labels = VGroup(*[
    Tex(tex).scale(0.5).next_to(axes.c2p(val, 0), DOWN, buff=0.15)
    for tex, val in [
        (r"\frac{\pi}{2}", PI / 2),
        (r"\pi", PI),
        (r"\frac{3\pi}{2}", 3 * PI / 2),
        (r"2\pi", TAU),
    ]
])
self.play(Write(pi_labels))
```

---

## Common LaTeX Snippets

```python
Tex(r"f(x) = \sin(x)")
Tex(r"\frac{d}{dx} f(x)")
Tex(r"\int_0^{\pi} \sin(x)\, dx")
Tex(r"\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")
Tex(r"\sin\theta = \frac{\text{opp}}{\text{hyp}}")
Tex(r"e^{i\pi} + 1 = 0")
TexText(r"For all $x \in \mathbb{R}$")
```

---

## Debugging Text

If LaTeX fails to compile, check the terminal for the LaTeX error. Common issues:
- Missing backslash: `sin` → `\sin`
- Unmatched braces
- Using `\text{}` inside `Tex()` (requires `amsmath` — usually fine with default template)
- Special characters that need escaping: `%`, `&`, `_` outside math mode
