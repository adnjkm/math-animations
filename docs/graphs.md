# Graphs, Axes & Curves in ManimGL

Source files: `manimlib/mobject/coordinate_systems.py`, `manimlib/mobject/number_line.py`, `manimlib/mobject/functions/parametric_curve.py`

---

## Axes

```python
axes = Axes(
    x_range=(-4, 4, 1),      # (min, max, step)
    y_range=(-2, 2, 0.5),
    width=10,                  # scene units wide
    height=6,                  # scene units tall
)
axes.move_to(ORIGIN)           # position in scene
self.play(ShowCreation(axes))
```

`x_range` / `y_range` follow `(min, max, step)` — step controls tick spacing.

---

## Coordinate Conversion

```python
# Scene point → data coordinates
axes.p2c(point)               # returns [x, y]

# Data coordinates → scene point
axes.c2p(x, y)                # returns np.array([px, py, 0])
axes.c2p(PI / 2, 1)           # point on the axes at (π/2, 1)
```

`c2p` is used constantly — for placing labels, drawing connections, and positioning dots on the graph.

---

## Graphing a Function

```python
# From the axes object (simplest)
curve = axes.get_graph(lambda x: np.sin(x), color=BLUE)
self.play(ShowCreation(curve))

# FunctionGraph (standalone, not tied to Axes)
curve = FunctionGraph(lambda x: x**2, x_range=[-3, 3], color=RED)
```

---

## ParametricCurve

**Critical:** `t_range` must have exactly 3 values `[min, max, step]`. Passing 2 values raises `ValueError: not enough values to unpack`.

```python
# WRONG — will crash
ParametricCurve(func, t_range=[0, TAU])

# CORRECT
ParametricCurve(func, t_range=[0, TAU, 0.01])
```

```python
# General usage
curve = ParametricCurve(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, TAU, 0.01],
    color=BLUE,
    stroke_width=3,
)

# Mapped through axes (most common for graphing)
curve = ParametricCurve(
    lambda t: axes.c2p(t, np.sin(t)),
    t_range=[0, TAU, 0.01],
    color=BLUE,
)
```

---

## Progressive Graph Reveal: pointwise_become_partial

Alternative to `always_redraw` when the curve is pre-computed. Reveals a graph progressively over time:
```python
graph = axes.get_graph(np.sin, color=BLUE)
shown_graph = graph.copy()
shown_graph.add_updater(
    lambda m: m.pointwise_become_partial(graph, 0, self.time / total_time)
)
self.add(shown_graph)
self.wait(total_time)
```

Use this when the curve shape is fixed and you just want to draw it over time. Use `always_redraw + ParametricCurve` (below) when the curve bounds change dynamically.
→ See `docs/advanced_patterns.md` for `self.time` and the time tracker pattern.

---

## Real-Time Curve Tracing with always_redraw

Build a curve that grows as a `ValueTracker` increases:

```python
theta = ValueTracker(0)

sin_curve = always_redraw(lambda: ParametricCurve(
    lambda t: axes.c2p(t, np.sin(t)),
    t_range=[0, max(theta.get_value(), 0.001), 0.01],  # avoids empty range
    color=BLUE,
    stroke_width=3,
))

self.add(sin_curve)
self.play(theta.animate.set_value(TAU), run_time=8, rate_func=linear)
```

The `max(..., 0.001)` guard prevents a zero-length range at t=0.

---

## NumberLine

```python
line = NumberLine(
    x_range=(-3, 3, 1),
    width=8,
    include_numbers=True,
)
line.move_to(ORIGIN)
self.play(ShowCreation(line))

# Get scene position of a value
point = line.n2p(2.5)          # number → point
value = line.p2n(point)        # point → number
```

---

## ThreeDAxes

For 3D scenes — adds a Z axis and supports depth:
```python
axes = ThreeDAxes(
    x_range=(-5, 5, 1),
    y_range=(-5, 5, 1),
    z_range=(0, 5, 1),
    width=10,
    height=10,
    depth=5,
)
```
→ See `docs/camera.md` for 3D camera setup. See `docs/advanced_patterns.md` for `VMobject.set_points_smoothly()` to plot ODE solutions through 3D axes.

---

## NumberPlane

A full coordinate plane with grid lines — useful as a background:

```python
plane = NumberPlane(
    x_range=(-7, 7, 1),
    y_range=(-4, 4, 1),
    background_line_style={"stroke_color": BLUE_D, "stroke_width": 1},
)
self.add(plane)
```

---

## Axis Labels

```python
# Built-in label method — pass a STRING, not a Tex object
# (get_axis_label calls Tex() internally; passing a Tex object crashes)
x_label = axes.get_x_axis_label("x")
y_label = axes.get_y_axis_label("f(x)")
self.play(Write(x_label), Write(y_label))

# To control font size, scale the result:
x_label.scale(0.7)

# Manual tick labels (common pattern)
labels = VGroup(*[
    Tex(tex).scale(0.5).next_to(axes.c2p(val, 0), DOWN, buff=0.15)
    for tex, val in [
        (r"\frac{\pi}{2}", PI / 2),
        (r"\pi", PI),
        (r"\frac{3\pi}{2}", 3 * PI / 2),
        (r"2\pi", TAU),
    ]
])
self.play(Write(labels))
```

---

## Connecting Elements Across Two Coordinate Systems

Useful for linking a unit circle to a graph (as in sine derivation animations):

```python
connect = always_redraw(lambda: DashedLine(
    circle_tip_point(),                              # world point from circle
    graph_axes.c2p(theta.get_value(), np.sin(theta.get_value())),
    color=RED,
    stroke_width=1.5,
))
self.add(connect)
```

---

## Dots on Graphs

```python
# Static dot at a data point
dot = Dot(axes.c2p(PI / 2, 1), color=YELLOW, radius=0.09)

# Moving dot that tracks a ValueTracker
dot = always_redraw(lambda: Dot(
    axes.c2p(theta.get_value(), np.sin(theta.get_value())),
    color=YELLOW,
    radius=0.09,
))
self.add(dot)
```

---

## Common Graph Patterns

### Animate a curve drawing itself
```python
curve = axes.get_graph(np.sin, color=BLUE)
self.play(ShowCreation(curve), run_time=3)
```

### Show a vertical drop from curve to x-axis
```python
x_val = PI / 2
drop = always_redraw(lambda: Line(
    axes.c2p(x_val, np.sin(x_val)),
    axes.c2p(x_val, 0),
    color=RED,
    stroke_width=2,
))
```

### Area under curve
```python
area = axes.get_area(curve, x_range=(0, PI), color=BLUE, opacity=0.3)
self.play(FadeIn(area))
```
