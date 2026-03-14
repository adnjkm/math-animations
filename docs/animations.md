# Animations, Updaters & ValueTracker in ManimGL

Source files: `manimlib/animation/`, `manimlib/mobject/value_tracker.py`

---

## Running Animations

```python
self.play(SomeAnimation(mob))                      # default run_time=1
self.play(SomeAnimation(mob), run_time=3)          # slower
self.play(SomeAnimation(mob), rate_func=linear)    # custom easing
self.play(Anim1(a), Anim2(b))                      # run simultaneously
self.wait(1)                                       # pause (also lets updaters run)
self.wait()                                        # pause until user presses Space/→
```

---

## Core Animation Classes

### Creation / Destruction
```python
ShowCreation(mob)             # draw the shape stroke-by-stroke
Write(mob)                    # for text — animate writing
DrawBorderThenFill(mob)       # outline then fill
FadeIn(mob)                   # appear by opacity
FadeOut(mob)                  # disappear by opacity
Uncreate(mob)                 # reverse of ShowCreation
```

### Transform
```python
Transform(a, b)               # morph a into b (a stays in scene as b's shape)
ReplacementTransform(a, b)    # morph a into b, then replace a with b in scene
FadeTransform(a, b)           # fade-morph a into b
MoveToTarget(mob)             # animate to mob.target (set with mob.generate_target())
TransformMatchingTex(a, b)    # morph matching LaTeX substrings, fade rest
TransformMatchingShapes(a, b) # match by geometric similarity
```

**MoveToTarget pattern:**
```python
mob.generate_target()
mob.target.scale(0.5).to_edge(UP).set_color(RED)
self.play(MoveToTarget(mob))
```

### Indication
```python
Indicate(mob)                 # brief scale pulse + color flash
Flash(mob)                    # radial burst of lines
Circumscribe(mob)             # draw a rectangle around it
Wiggle(mob)                   # wobble in place
FocusOn(point)                # brief dot flash at a point
```

### Movement
```python
MoveAlongPath(mob, path)      # move along a VMobject path
Rotate(mob, angle=PI)         # rotate in place
```

### Numbers
```python
ChangingDecimal(decimal_mob, func)          # animate decimal value changing
ChangeDecimalToValue(decimal_mob, value)    # animate to a specific value
CountInFrom(decimal_mob, start_value)       # count up from start_value to current
```

### Indication / Growth
```python
GrowArrow(arrow)              # grow an arrow from tail to tip
GrowFromCenter(mob)           # scale up from 0 at center
```

### UpdateFromFunc / UpdateFromAlphaFunc
```python
# UpdateFromFunc: called every frame — useful when driving a complex mobject
self.play(UpdateFromFunc(graph, lambda g: g.become(recompute_graph())))

# UpdateFromAlphaFunc: called with alpha in [0,1] — for value interpolation
self.play(UpdateFromAlphaFunc(
    entry,
    lambda m, a: m.set_value(start + a * (end - start))
))
```

---

## Composing Animations

### AnimationGroup — run together
```python
self.play(AnimationGroup(
    FadeIn(a),
    ShowCreation(b),
    Write(c),
))
```

### Succession — run sequentially in one `play` call
```python
self.play(Succession(
    ShowCreation(circle),
    Write(label),
    FadeIn(arrow),
))
```

### LaggedStart — stagger across submobjects
```python
# Apply the same animation to each item with a stagger
self.play(LaggedStart(*[FadeIn(mob) for mob in my_group], lag_ratio=0.3))

# lag_ratio=0 means all at once, lag_ratio=1 means fully sequential
```

### LaggedStartMap — apply one animation type to all items
```python
self.play(LaggedStartMap(FadeIn, items, lag_ratio=0.2))
self.play(LaggedStartMap(Write, equations, lag_ratio=0.5, run_time=3))
```

### ShowSubmobjectsOneByOne / ShowIncreasingSubsets
```python
self.play(ShowSubmobjectsOneByOne(group, run_time=2))   # add one at a time
self.play(ShowIncreasingSubsets(group, rate_func=linear))  # show n=1, then 2, then 3...
```

---

## Rate Functions (Easing)

Pass as `rate_func=` to `self.play()`:

| Function | Behavior |
|----------|----------|
| `smooth` | Default — ease in and out (S-curve) |
| `linear` | Constant speed |
| `rush_into` | Start fast, slow down |
| `rush_from` | Start slow, speed up |
| `there_and_back` | Go and return |
| `wiggle` | Oscillate |
| `exponential_decay` | Fast then slow |
| `double_smooth` | Extra smooth S-curve |

```python
self.play(mob.animate.shift(RIGHT), rate_func=linear, run_time=4)
```

---

## The `.animate` Shorthand

Chain any transformation and it animates automatically:

```python
self.play(mob.animate.shift(RIGHT * 2))
self.play(mob.animate.scale(0.5).to_edge(UP))
self.play(mob.animate.set_color(RED).rotate(PI / 4))
```

Note: `.animate` snapshots start/end state and interpolates — it does NOT run intermediate Python code per frame. For frame-by-frame control, use updaters.

---

## ValueTracker

An invisible object that holds an animatable float value:

```python
t = ValueTracker(0)           # initialize at 0
t.get_value()                 # read current value
t.set_value(2.5)              # set immediately (no animation)

# Animate the value changing
self.play(t.animate.set_value(TAU), run_time=4, rate_func=linear)
```

Multiple trackers can drive multiple things simultaneously:

```python
self.play(
    t.animate.set_value(TAU),
    opacity_tracker.animate.set_value(0),
    run_time=3,
)
```

---

## Updaters

Updaters are functions called every frame. They enable continuous, reactive motion:

```python
# Simple updater — takes the mobject as argument
dot.add_updater(lambda d: d.move_to(some_other_mob.get_center()))

# Time-based updater — takes mobject and dt (delta time in seconds)
mob.add_updater(lambda m, dt: m.rotate(dt * 0.5))

# Remove an updater
dot.remove_updater(my_func)

# Remove all updaters
dot.clear_updaters()
```

Updaters run during:
- `self.play(...)` — every frame of the animation
- `self.wait(duration)` — every frame of the wait

---

## always_redraw

Convenience wrapper: creates a fresh mobject each frame by calling a lambda. Cleaner than `add_updater` when the whole object needs to rebuild:

```python
# Redraws the line from scratch every frame
radius = always_redraw(lambda: Line(center, tip_point(), color=WHITE))
self.add(radius)

# Now animate something that tip_point() depends on
self.play(theta.animate.set_value(PI), run_time=3)
# radius automatically follows
```

Common with:
- Lines/arrows that track moving points
- Curves that grow over time (with ParametricCurve + ValueTracker)
- Labels that must stay positioned relative to a moving object

---

## ValueTracker + always_redraw Pattern

The core pattern for driving dynamic scenes:

```python
theta = ValueTracker(PI / 3)

# Geometry that updates with theta
radius_line = always_redraw(lambda: Line(
    center,
    center + R * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
))

angle_arc = always_redraw(lambda: Arc(
    radius=0.4,
    start_angle=0,
    angle=max(theta.get_value(), 0.001),  # guard against zero
    arc_center=center,
    color=YELLOW,
))

self.add(radius_line, angle_arc)

# Now sweeping theta drives everything
self.play(theta.animate.set_value(TAU), run_time=6, rate_func=linear)
```

---

## Scene Management

```python
self.add(mob)                  # add to scene instantly (no animation)
self.remove(mob)               # remove instantly
self.clear()                   # remove all mobjects (use at top of construct() when re-running)
self.bring_to_front(mob)       # z-order: move to top
self.bring_to_back(mob)        # z-order: move to bottom
```

---

## save_state / restore_state

Snapshot and restore a mobject's appearance:

```python
mob.save_state()
self.play(mob.animate.scale(2).set_color(RED))
self.play(Restore(mob))        # animates back to saved state
```
