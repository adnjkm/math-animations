# Advanced ManimGL Patterns
# (from 3b1b/videos source)

Source: https://github.com/3b1b/videos — real production scenes used in 3Blue1Brown videos.

---

## Key Classes Not in the Basics

### Dots
```python
Dot(point, color=YELLOW, radius=0.09)    # standard filled circle dot
TrueDot(point, color=YELLOW)             # GPU-rendered, precise
GlowDot(color=YELLOW, radius=0.25)       # glowing dot with halo effect

# GlowDot is in Group (not VGroup) — it's not a VMobject
dots = Group(GlowDot(color=color) for color in colors)
```

### TracingTail
Leaves a fading trail behind a moving object:
```python
tail = VGroup(
    TracingTail(dot, time_traced=3).match_color(dot)
    for dot in dots
)
self.add(tail)
# As dot moves, tail follows and fades over 3 seconds
```

### DecimalNumber / Integer
Animatable number displays:
```python
value = DecimalNumber(3.14, num_decimal_places=2)
integer = Integer(42, font_size=40)

# Animate counting up
self.play(CountInFrom(value, 0))          # counts from 0 to current value
self.play(ChangeDecimalToValue(value, 9.99))
```

### SurroundingRectangle
```python
rect = SurroundingRectangle(mob, buff=0.2)
rect.set_stroke(YELLOW, 2)
rect.round_corners(0.1)                   # rounded corners

# Move it to wrap a different object (animate-able)
self.play(rect.animate.surround(mob2, buff=0.1))
```

### Brace
```python
brace = Brace(mob, LEFT, buff=SMALL_BUFF)
label = brace.get_text("label")
label.next_to(brace, LEFT)
self.play(GrowFromCenter(brace))
```

### ArrowTip (standalone)
```python
tip = ArrowTip(angle=-90 * DEG)           # pointing downward
tip.set_width(0.25)
tip.move_to(some_point, DOWN)
```

---

## Tex Patterns from Production Code

### `t2c` shorthand and `font_size`
```python
# t2c is shorthand for tex_to_color_map — use this everywhere
eq = Tex(
    R"f(x) = \sin(x)",
    t2c={"x": BLUE, R"\sin": YELLOW},
    font_size=48,
)

# Multi-line LaTeX in triple-quoted raw strings
eq = Tex(
    R"""
    \frac{\mathrm{d} x}{\mathrm{~d} t} = \sigma(y - x) \\
    \frac{\mathrm{d} y}{\mathrm{~d} t} = x(\rho - z) - y
    """,
    t2c={"x": RED, "y": GREEN, "z": BLUE},
    font_size=30,
)
```

### Indexing into Tex by substring
```python
eq = Tex(R"\sin(\theta) = \frac{\text{opp}}{\text{hyp}}")
eq[R"\sin"].set_color(YELLOW)          # access part by LaTeX substring
eq[R"\theta"].set_color(BLUE)
```

### make_number_changeable — animated placeholders
Replace a number token with an animatable value:
```python
template = Tex(R"\vec{E}_{0}")
dec = template.make_number_changeable("0")
dec.set_value(5)                        # changes the "0" to "5"

# Copy template with different values
for n in range(1, 10):
    dec.set_value(n)
    sym = template.copy()
```

### set_backstroke — readable text over 3D
```python
equations.fix_in_frame()
equations.to_corner(UL)
equations.set_backstroke()              # adds dark outline for readability over 3D backgrounds
```

---

## VGroup with Generator Expressions

Modern Python syntax (used throughout 3b1b's code):
```python
# New style — generator inside VGroup()
dots = VGroup(Dot(axes.c2p(x, 0)) for x in x_values)

# Equivalent old style
dots = VGroup(*[Dot(axes.c2p(x, 0)) for x in x_values])

# Group (non-VMobject) with generator
images = Group(ImageMobject(path).set_height(1.5) for path in paths)
```

**Rule:** Use `VGroup` for VMobjects (shapes, text, etc.), `Group` for non-VMobjects (`ImageMobject`, `GlowDot`, etc.).

---

## Camera: fix_in_frame

Pin a mobject to screen space so it doesn't move with the camera — essential for HUD labels in 3D scenes:
```python
title = Tex("Lorenz Attractor")
title.fix_in_frame()
title.to_corner(UL)
self.add(title)

# Or fix after the fact
eq.fix_in_frame()

# Also works on arrows, axes labels, anything
axes_label.fix_in_frame()
```

→ See `docs/camera.md` for full camera reference.

---

## Progressive Graph Reveal: pointwise_become_partial

Alternative to `always_redraw + ParametricCurve` for revealing a pre-computed graph:
```python
graph = axes.get_graph(np.sin, color=BLUE)
graph_ghost = graph.copy().set_stroke(opacity=0.3)  # faint full graph preview

shown_graph = graph.copy()
shown_graph.add_updater(
    lambda m: m.pointwise_become_partial(graph, 0, self.time / total_time)
)
self.add(graph_ghost, shown_graph)
self.wait(total_time)
```

**When to use which:**
- `pointwise_become_partial`: best when graph is pre-computed and you just want to reveal it over time
- `always_redraw + ParametricCurve`: best when the curve bounds change dynamically (e.g., driven by `ValueTracker`)

→ See `docs/graphs.md` for the `always_redraw` pattern.

---

## Self-Incrementing Time Tracker

Use `self.time` for scene time in updaters. Or create an explicit tracker:
```python
# Scene time is always available as self.time
shown_graph.add_updater(lambda m: m.pointwise_become_partial(graph, 0, self.time / 10))

# Or: explicit incrementing ValueTracker
t_tracker = ValueTracker(0)
t_tracker.add_updater(lambda m, dt: m.increment_value(dt))
self.add(t_tracker)
get_t = t_tracker.get_value

# Now use get_t() in other updaters
dot.add_updater(lambda m: m.move_to(axes.c2p(get_t(), np.sin(get_t()))))
```

---

## 3D Objects

### ThreeDAxes
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

### Sphere
```python
sphere = Sphere(radius=3)
sphere.set_color(BLUE, 0.5)                  # color + opacity
sphere.always_sort_to_camera(self.camera)    # REQUIRED for correct rendering (prevents z-order glitches)

mesh = SurfaceMesh(sphere, resolution=(51, 26))
mesh.set_stroke(WHITE, 2, 0.2)
```

### 3D Material Properties
```python
mob.set_gloss(0.5)            # specularity (0 = matte, 1 = shiny)
mob.set_shadow(0.2)           # self-shadow darkness
mob.set_reflectiveness(0.3)   # environment reflectance
mob.set_clip_plane(IN, 0)     # clip everything behind the XY plane
```

### Clipping
```python
# Clip a 3D object to only show half of it
sphere.set_clip_plane(IN, 0)                         # hide the back
self.play(sphere.animate.set_clip_plane(IN, radius)) # animate clip plane moving
```

---

## Smooth Curves from Point Arrays

Build a VMobject curve from arbitrary 3D point data (e.g., ODE solutions):
```python
# points is an (N, 3) numpy array
curve = VMobject()
curve.set_points_smoothly(axes.c2p(*points.T))  # maps data coords through axes
curve.set_stroke(BLUE, 2, opacity=0.5)
```

Combine with ODE integration:
```python
from scipy.integrate import solve_ivp

solution = solve_ivp(system_func, t_span=(0, 30), y0=initial_state, t_eval=np.arange(0, 30, 0.01))
points = solution.y.T   # shape (N, 3)
curve = VMobject().set_points_smoothly(axes.c2p(*points.T))
```

---

## Vector Fields and Stream Lines

```python
vector_field = VectorField(
    func,               # function: 3D point → 3D vector
    axes,
    density=4,
    stroke_width=5,
    stroke_opacity=0.5,
)

stream_lines = StreamLines(
    func, axes,
    density=5,
    n_samples_per_line=10,
    solution_time=1,
    stroke_color=WHITE,
    stroke_width=3,
)
animated_lines = AnimatedStreamLines(
    stream_lines,
    line_anim_config=dict(time_width=0.5),
    rate_multiple=0.25,
)
self.add(animated_lines)
```

---

## ComplexPlane and ComplexValueTracker

For complex analysis / Laplace transform / Fourier scenes:
```python
s_plane = ComplexPlane((-3, 3), (-3, 3))
s_plane.add_coordinate_labels(font_size=20)

# Track a complex value
s_tracker = ComplexValueTracker(complex(0, 2))       # starts at 2i
dot = TrueDot()
dot.add_updater(lambda m: m.move_to(s_plane.n2p(s_tracker.get_value())))

# Animate moving in complex plane
self.play(s_tracker.animate.set_value(complex(-0.5, 2)))

# Conjugate tracking
s_tracker2.add_updater(lambda m: m.set_value(s_tracker.get_value().conjugate()))
```

---

## MoveToTarget Pattern

Animate a mobject to a pre-defined target state:
```python
mob.generate_target()
mob.target.scale(0.5).to_edge(UP)
mob.target.set_color(RED)
self.play(MoveToTarget(mob))

# Useful for multiple objects simultaneously
for mob in mobs:
    mob.generate_target()
    mob.target.shift(RIGHT * n)
self.play(LaggedStart(*[MoveToTarget(m) for m in mobs], lag_ratio=0.1))
```

---

## UpdateFromFunc / UpdateFromAlphaFunc

```python
# UpdateFromFunc: called every frame during the animation
self.play(UpdateFromFunc(graph, lambda g: g.become(get_new_graph())))

# UpdateFromAlphaFunc: called with alpha ∈ [0, 1] for the animation duration
self.play(UpdateFromAlphaFunc(
    entry,
    lambda m, a: m.set_value(start + a * (end - start))
))
```

---

## Staggered Animations

```python
# LaggedStartMap — apply one animation type to all items with stagger
self.play(LaggedStartMap(FadeIn, items, lag_ratio=0.2))
self.play(LaggedStartMap(Write, equations, lag_ratio=0.5, run_time=3))

# LaggedStart — stagger arbitrary animations
self.play(LaggedStart(
    *[mob.animate.shift(UP) for mob in mobs],
    lag_ratio=0.15,
))

# ShowSubmobjectsOneByOne — reveal submobjects sequentially
self.play(ShowSubmobjectsOneByOne(group, run_time=2))

# ShowIncreasingSubsets — show first 1, then 2, then 3... submobjects
self.play(ShowIncreasingSubsets(group, rate_func=linear))
```

---

## Utility Functions

```python
clip(value, min_val, max_val)                      # clamp a value
inverse_interpolate(min_val, max_val, value)        # what alpha gives value?
interpolate_color_by_hsl(color1, color2, alpha)     # HSL color interpolation
color_gradient([BLUE, RED], n=10)                   # list of n evenly spaced colors
color_gradient([BLUE, RED], n=10, interp_by_hsl=True)  # HSL interpolation
midpoint(point1, point2)                            # geometric midpoint
get_norm(vector)                                    # vector magnitude

# Itertools are imported as `it` by default
it.count(start, step)
it.count(1)                                         # 1, 2, 3, ...
```

---

## Space Out Submobjects

```python
group.space_out_submobjects(1.3)    # push submobjects 30% further from center
self.play(group.animate.space_out_submobjects(0.8))  # animate compress
```

---

## color_gradient for Coloring Groups

```python
colors = color_gradient([BLUE_E, BLUE_A], len(items))
for item, color in zip(items, colors):
    item.set_color(color)

# Or directly on submobjects:
group.set_color_by_gradient(BLUE, RED)
group.set_submobject_colors_by_gradient(BLUE, RED)
```

---

## Constants

```python
FRAME_WIDTH    # scene width in scene units (~14.2)
FRAME_HEIGHT   # scene height in scene units (~8.0)
RIGHT_SIDE     # right edge of frame
LEFT_SIDE      # left edge of frame
DEGREES        # same as DEG
SMALL_BUFF     # small gap (~0.1)
MED_SMALL_BUFF # slightly larger gap
MED_LARGE_BUFF # medium-large gap
LARGE_BUFF     # large gap (~0.75)
```

---

## Production Code Organization Pattern

3b1b's videos use a shared import at the top of every scene file:
```python
from manim_imports_ext import *   # imports manimlib + custom characters/assets
```

Large videos are split into multiple files (e.g., `helpers.py` for shared custom classes, `main.py` for actual scenes). Helper files define reusable `VGroup` subclasses, utility functions, and custom animations.

When building your own complex scenes, consider:
- A `helpers.py` for reusable components (custom bar charts, diagram builders, etc.)
- Subclassing `VGroup` for complex visual elements that need their own logic
