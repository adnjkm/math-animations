---
name: police_ballistics
description: Lessons learned and thought process from building the ballistic forensics animation (police.py)
type: project
---

# Project: Ballistic Forensics Animation (`police.py`)

A multi-phase animation for a police firearms department showing bullet evidence analysis, weapon identification, and gang network mapping.

---

## Scene Structure

Seven phases, each building on the last:

1. **Grid** — 4×4 spread of bullets by caliber, interleaved randomly
2. **Sort** — bullets fly into 4 caliber clusters (2×2 each), rounded boxes labeled
3. **Machine** — one group (9mm) funnels into a "Ballistic Database" machine → outputs "Glock 17"
4. **Business card** — full-screen card with gun specs and "SEARCHING..." placeholder
5. **Tape scroll** — horizontal name list scrolls left until match centers; blinks 3×
6. **Owner reveal** — card fills with suspect's details after match
7. **Network graph** — suspect as center node, 5 connected members revealed then apprehended

---

## Bullet Shape: Rectangle + Arc

The key to a convincing bullet silhouette is a `Rectangle` body with an `Arc` semicircle tip precisely aligned to its top edge:

```python
def make_bullet(width, height, color=WHITE):
    case = Rectangle(width=width, height=height)
    tip = Arc(
        radius=width / 2,
        start_angle=0,
        angle=PI,
        arc_center=np.array([0.0, height / 2.0, 0.0]),
    )
    b = VGroup(case, tip)
    b.set_fill(color, opacity=0.9)
    b.set_stroke(color, 1.5)
    return b
```

- `arc_center` at `[0, height/2, 0]` places the semicircle endpoints exactly at the rectangle's top corners
- `VGroup` propagates `.set_fill` / `.set_stroke` to both parts
- Total visual height = `height + width/2` (rectangle + semicircle radius) — remember this when spacing

---

## Grid Layout: Why `arrange_in_grid` Fails for Tall Narrow Objects

Bullets are inherently tall and narrow (~0.16–0.30 wide × 0.68–1.40 tall). Using `arrange_in_grid` with a uniform `buff` produces a "thin pillar" — the equal spacing looks fine horizontally but the rows collapse together vertically.

**Fix:** Manual `move_to` with separate `col_spacing` and `row_spacing` values:

```python
col_spacing = 1.9   # >> bullet width — forces horizontal spread
row_spacing = 1.3   # calibrated to scaled bullet height
```

This is the general lesson: **when objects have extreme aspect ratios, `arrange_in_grid` with a single buff will always look unbalanced in one axis — use manual positioning instead.**

---

## Grid Scale → Sort Scale Pattern

Bullets at full size with `row_spacing=1.7` still nearly overlapped (gap ~0.16 units). The solution is a two-phase size approach:

1. **Grid phase**: scale bullets down (`GRID_SCALE = 0.55`) before placing in grid — clear visible gaps between all bullets
2. **Sort phase**: animate back to full size as they fly into groups

Implementation detail: the temp groups used to define sort target positions must be built from **fresh full-size bullets**, not copies of the already-scaled grid bullets. Otherwise the layout positions are computed for small bullets and the scaled-up result will overlap.

```python
# WRONG — copies inherit current (small) scale
tg = VGroup(*[bullets[i].copy() for i in gm[gid]])

# CORRECT — fresh full-size bullets define the layout
sample = make_bullet(GD[gid]["w"], GD[gid]["h"], GD[gid]["color"])
tg = VGroup(*[sample.copy() for _ in gm[gid]])
```

Then during `generate_target()`:
```python
bullets[bi].target.move_to(temp_groups[gid][li].get_center())
bullets[bi].target.scale(1.0 / GRID_SCALE)  # restore full size
```

`MoveToTarget` animates both position and scale simultaneously — the bullets grow as they fly.

---

## Horizontal Tape Scroll

To scroll a name list from off-screen right until a specific name lands at center:

```python
tape.align_to(RIGHT_SIDE, LEFT)   # push entire tape just off right edge of frame
self.add(tape)
shift_amt = tape[MATCH_IDX].get_center()[0]   # how far right of center the match starts
self.play(tape.animate.shift(LEFT * shift_amt), run_time=4.0, rate_func=linear)
```

- `RIGHT_SIDE` is ManimGL's constant for the right screen edge (`[7.11, 0, 0]`)
- `align_to(RIGHT_SIDE, LEFT)` snaps the tape's **left edge** to the right screen edge — full tape starts off-screen
- The match's x-coordinate after tape is placed = exactly how much to shift left so it ends at x=0

---

## Business Card Layout

For a screen-filling card (use ~10.5 × 5.2 units for a 16:9 scene):

```python
card = Rectangle(width=10.5, height=5.2)
card.set_stroke(BLUE_B, 2.5)
card.set_fill(GREY_E, opacity=0.93)
card.move_to(UP * 0.9)   # shift up to leave room for tape below

header_strip = Rectangle(width=10.5, height=0.85)
header_strip.set_fill(BLUE_E, opacity=0.40)
header_strip.align_to(card, UP)   # pin strip to top of card
```

Build content top-down with `next_to(..., DOWN, buff=...)` chains. Left-align text blocks to a consistent margin with:
```python
gun_block.align_to(card.get_left() + RIGHT * 0.55, LEFT)
```

---

## `make_node` Scoping with `checkpoint_paste`

Defining helper functions at module level causes `NameError` when `checkpoint_paste` sends only a portion of `construct()` into the IPython shell — the module-level function exists in the file but not in the shell's namespace unless the full scene has been booted since the last restart.

**Rule:** Any helper function used inside `construct()` that checkpoint_paste cells depend on should be defined **inside `construct()`** as a local function. It will always be in scope for any cell that runs within construct, regardless of what was pasted before.

```python
def construct(self):
    def make_node(color, r=0.22):   # local — always available to checkpoint_paste
        ...
```

---

## `EndScene` Is Not a Crash

`EndScene` is ManimGL's normal mechanism for closing the interactive window (raised by `is_window_closing()` when the user presses Cmd+Q or closes the window). If it appears during `self.play()`, the window was closed — not a code error. Fix: re-run `ManimRunScene` to get a fresh window.

---

## Aesthetic Notes (Grover Video Style)

Inspired by `_2025/grover/state_vectors.py`:

- **Background palette**: `GREY_E` fills, `BLUE_E` header strips at ~40% opacity
- **Accent colors**: `BLUE_B` for highlights, `TEAL` for match/confirmed states, `GREY_B/C` for secondary text
- **Machine decoration**: interior `h_lines` (3 horizontal lines at `dy = -0.45, 0.0, 0.45`) add depth without clutter
- **Node style**: `VGroup(glow_circle, core_dot)` — glow circle at 10% fill opacity + 30% stroke opacity wrapping a solid `Dot`. Set `.animate.set_color()` on the VGroup to recolor both parts simultaneously
- **Progressive reveal**: `LaggedStart` with small `lag_ratio` (0.04–0.15) for bullets; single-step `run_time=0.55` for network edges
- **Apprehension**: `SurroundingRectangle` flash → `FadeOut(flash)` + dim to `GREY_C` in same play call

---

## MoveToTarget Pattern for Mass Rearrangement

When animating many objects to new positions simultaneously:

```python
# Set up targets
for each_obj:
    obj.generate_target()
    obj.target.move_to(destination)
    obj.target.scale(...)   # optional transform at destination

# Animate all at once with stagger
self.play(LaggedStart(
    *[MoveToTarget(obj) for obj in objects],
    lag_ratio=0.04, run_time=2.0,
))
```

This is cleaner than `Transform` for position-only moves and supports simultaneous scale/color changes on the target.

---

## Network Graph Pattern

```python
# Node: glow + core so set_color works on whole VGroup
def make_node(color, r=0.22):
    glow = Circle(radius=r * 2.0)
    glow.set_fill(color, opacity=0.10)
    glow.set_stroke(color, 1.0, opacity=0.30)
    core = Dot(radius=r, color=color)
    return VGroup(glow, core)

# Progressive edge + node reveal
reveal_steps = [("A", "B", ["B"]), ("A", "C", []), ...]
for a, b, new_nodes in reveal_steps:
    edge = Line(NP[a], NP[b]).set_stroke(GREY_C, 1.5, opacity=0.5)
    anims = [ShowCreation(edge)]
    for n in new_nodes:
        anims += [FadeIn(nodes[n]), Write(node_labels[n])]
    self.play(*anims, run_time=0.55)

# Apprehend: flash rect → dim to grey
flash = SurroundingRectangle(nodes[name], buff=0.1, color=RED)
self.play(ShowCreation(flash), run_time=0.2)
self.play(
    nodes[name].animate.set_color(GREY_C),
    node_labels[name].animate.set_color(GREY_C),
    FadeOut(flash),
    run_time=0.35,
)
```
