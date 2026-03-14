# Camera, 3D & Interactive Controls in ManimGL

Source files: `manimlib/camera/camera_frame.py`, `manimlib/scene/scene.py`, `manimlib/scene/interactive_scene.py`

---

## Camera Frame Basics

The camera is accessed via `self.frame`. It handles panning, zooming, and 3D rotation.

```python
# Reorient by Euler angles (degrees) — most common for 3D
self.frame.reorient(theta, phi, gamma)
self.frame.reorient(45, 70, 0)                            # orbit + tilt
self.frame.reorient(30, 60, 0, center=(0, 0, 0), height=8)  # with position and zoom

# Pan
self.frame.shift(RIGHT * 2)
self.frame.move_to(some_mobject)

# Zoom
self.frame.scale(0.5)                   # zoom in (smaller frame = closer)
self.frame.set_field_of_view(60 * DEG)
self.frame.set_focal_distance(10)

# Animate any camera operation
self.play(self.frame.animate.reorient(90, 60, 0))
self.play(self.frame.animate.shift(UP * 2).scale(0.8))
```

---

## Euler Angles

| Angle | Axis | Effect |
|-------|------|--------|
| theta | Z (vertical) | Horizontal orbit around the scene |
| phi | XY plane | Vertical tilt / elevation |
| gamma | Camera forward | Roll (rotation around camera axis) |

Default 2D view: `theta=0, phi=0, gamma=0` (camera looking straight down -Z).

---

## Individual Axis Control

```python
self.frame.set_theta(45 * DEG)
self.frame.set_phi(70 * DEG)
self.frame.set_gamma(0 * DEG)

# Incremental
self.frame.increment_theta(0.1)
self.frame.increment_phi(0.05)

# Arbitrary axis
self.frame.rotate(angle=PI / 4, axis=UP)
```

---

## Reading Camera State

```python
self.frame.get_euler_angles()            # [theta, phi, gamma] in radians
self.frame.get_center()
self.frame.get_width()
self.frame.get_height()
self.frame.get_implied_camera_location() # actual 3D camera position
self.frame.get_view_matrix()             # full 4x4 affine view matrix
self.frame.get_inv_view_matrix()
```

---

## Ambient Rotation (continuous spin)

```python
# Add as updater — camera slowly rotates throughout the scene
self.frame.add_ambient_rotation(angular_speed=0.02)

# Remove it
self.frame.clear_updaters()
```

---

## Coordinate Transforms

```python
# World → fixed frame (screen space)
self.frame.to_fixed_frame_point(world_point)

# Fixed frame → world
self.frame.from_fixed_frame_point(fixed_point)
```

---

## Mouse Controls (InteractiveScene)

| Input | Action |
|-------|--------|
| Click + drag | Pan camera (shifts `camera.frame`) |
| Hold `d` + move mouse | 3D rotate — left/right → theta, up/down → phi |
| Scroll wheel | Zoom about cursor position |

Sensitivity constants (in `scene.py`):
```python
pan_sensitivity: float = 0.5   # 3D rotation speed multiplier
scroll_sensitivity: float = 20  # zoom speed multiplier
drag_to_pan: bool = True        # whether plain drag pans
```

---

## Keyboard Controls (InteractiveScene)

### Camera
| Key | Action |
|-----|--------|
| `r` | Reset camera to default (animated) |
| `d` (hold) + mouse | 3D pan/rotate |
| `Shift + d` | Copy `reorient(...)` call for current position to clipboard |

### Undo / Quit
| Key | Action |
|-----|--------|
| `Cmd + z` | Undo last scene state |
| `Cmd + Shift + z` | Redo |
| `Cmd + q` | Quit interaction |
| `Space` or `→` | Advance past `self.wait()` |

### Selection
| Key | Action |
|-----|--------|
| `Ctrl` (hold, tap) | Select mobject under cursor |
| `Ctrl` (hold, drag) | Box-select multiple mobjects |
| `Cmd + a` | Select all |
| `Cmd + t` | Toggle top-level vs submobject selection |
| `Backspace` | Delete selection |
| `Cmd + c` | Copy selected mobject IDs |
| `Cmd + v` | Paste (by ID, or Tex/Text from clipboard string) |
| `Cmd + x` | Cut |
| `Cmd + g` | Group selection |
| `Cmd + Shift + g` | Ungroup |

### Transformation (with selection active)
| Key | Action |
|-----|--------|
| `g` (hold) | Grab and move freely |
| `h` (hold) | Grab, constrained to X axis |
| `v` (hold) | Grab, constrained to Y axis |
| `z` (in grab mode) | Grab, constrained to Z axis |
| `t` (hold) | Resize uniformly |
| `Shift + t` | Resize from corner |
| Arrow keys | Nudge selection |
| `Shift + arrows` | Larger nudge |
| `c` | Toggle color palette |

### Other
| Key | Action |
|-----|--------|
| `i` | Toggle cursor/crosshair display |
| `Shift + c` | Copy current cursor position (as tuple) to clipboard |

Key bindings (except `r`, `d`, undo/redo/quit) can be remapped in `custom_config.yml` under `manim_config.key_bindings`.

---

## Selection System

- `self.selection` — `Group` of currently selected mobjects
- `self.unselectables` — mobjects excluded from selection (UI elements)
- `self.select_top_level_mobs` — toggle whole-object vs submobject selection
- `save_state()` is auto-called before grab/resize so undo works correctly

---

## Window Configuration

```python
# In custom_config.yml or via CLI:
# window_position: UR / UL / DL / DR / OO (corner or center)
# monitor_index: 0 / 1 (for multi-monitor setups)
```

Window defaults to half the monitor width, maintaining aspect ratio.

---

## fix_in_frame — HUD Elements in 3D Scenes

Pin mobjects to screen space so they don't move with the camera. Essential for labels, equations, and UI that should stay fixed while the 3D scene moves:

```python
title = Tex("Lorenz Attractor")
title.fix_in_frame()
title.to_corner(UL)
self.add(title)

# Also useful for: equations panels, axis labels, progress indicators
equations.fix_in_frame()
equations.set_backstroke()   # adds dark outline — improves readability over 3D backgrounds
```

---

## 3D Scene Pattern

```python
from manimlib import *

class My3DScene(InteractiveScene):
    def construct(self):
        self.clear()

        # Set 3D camera angle
        self.frame.reorient(45, 70, 0)

        # Add 3D objects
        surface = ParametricSurface(
            lambda u, v: np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v)]),
            u_range=[0, TAU],
            v_range=[0, PI],
        )
        self.play(ShowCreation(surface))

        # Animate camera orbit
        self.play(self.frame.animate.reorient(135, 70, 0), run_time=3)

        # Continuous spin
        self.frame.add_ambient_rotation(0.02)
        self.wait(5)
```
