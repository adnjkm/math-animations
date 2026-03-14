# Manim (ManimGL) — Core Reference

Source: https://github.com/3b1b/manim

## GitHub Repo

This project lives at **https://github.com/adnjkm/math-animations**. Push new scenes and doc updates there after each session.

---

## Living Documentation — Keep This Sharp

This file and the `docs/` files are a continuously improving brain for ManimGL. Every session should leave them better than it found them. Follow these rules:

**When you encounter a new error or unexpected behavior:**
1. Fix it
2. Ask: *why did this happen?* — not just what was wrong, but what assumption or knowledge gap caused it
3. Abstract that into a general rule, not just a one-off fix
4. Add it to `docs/errors.md` with the full thought process: what broke, why, what the wrong mental model was, and the check that prevents it next time
5. If it reveals a gap in a topic doc (`docs/text.md`, `docs/graphs.md`, etc.), update that doc too

**When you learn something new about the ManimGL API:**
- Add it to the relevant `docs/` file, not buried in conversation
- If it doesn't fit an existing file, consider whether a new one is warranted

**Cross-referencing between docs:**
When a new piece of information genuinely connects to something in another doc, add a targeted inline reference at that specific point — not at the top, not broadly, but exactly where the connection is relevant. Example: a note in `graphs.md` about `always_redraw` might link to `animations.md` at the `always_redraw` section. This lets Claude follow real conceptual connections rather than loading everything upfront. Don't add cross-references just for completeness — only when a reader of that specific line would genuinely benefit from jumping to the other doc.

**The goal:** build the most capable ManimGL reference possible so that future sessions start smarter, make fewer mistakes, and spend more time animating.

---

## Topic-Specific References

For detailed API info beyond this file, read the relevant doc:

- **Text & LaTeX** → `@docs/text.md`
- **Graphs, Axes & Curves** → `@docs/graphs.md`
- **Animations, Updaters & ValueTracker** → `@docs/animations.md`
- **Camera, 3D & Interactive Controls** → `@docs/camera.md`
- **Advanced patterns from 3b1b/videos** → `@docs/advanced_patterns.md` — real production techniques: GlowDot, TracingTail, VectorField, ComplexPlane, fix_in_frame, ODE curves, generator VGroup syntax, and more
- **3b1b video scene index** → `@docs/video_index.md` — one-line summary + key visualizations for every video in the repo, organized by year; scan this when the user's request resembles a known topic, then fetch the relevant file from `https://raw.githubusercontent.com/3b1b/videos/master/<path>` for real code examples
- **Past errors & how to avoid them** → `@docs/errors.md` — read this before writing any new ManimGL code

---

## When to Reference 3b1b's Video Code

Before writing a new scene, check `docs/video_index.md`. If the user's topic matches a known video (e.g. "Fourier transform" → `_2018/fourier.py`, "convolution" → `_2022/convolutions/`, "eigenvalues" → `_2024/linalg/eigenlecture.py`), fetch that file for real working code patterns at the relevant complexity. The index has one-line summaries and key visualizations so you can scan it fast.

Fetch video code at: `https://raw.githubusercontent.com/3b1b/videos/master/<path>`

---

## How to Look Up Manim Details

If something isn't covered here or in the docs above, fetch directly from GitHub — do NOT scan the local filesystem:

- `https://raw.githubusercontent.com/3b1b/manim/master/<path>`

Key files by topic:
- Scene logic → `manimlib/scene/scene.py`, `manimlib/scene/interactive_scene.py`
- Animations → `manimlib/animation/<file>.py`
- Mobjects → `manimlib/mobject/<file>.py`
- Coordinate systems → `manimlib/mobject/coordinate_systems.py`
- Constants / colors → `manimlib/constants.py`

---

## Development Environment

The user runs ManimGL from **Sublime Text** using a custom plugin (`manim_plugins.py`) with the **Terminus** package — NOT a Jupyter notebook.

- `ManimRunScene` runs `manimgl <file>.py <ClassName>` in a Terminus terminal tab
- This boots a live `InteractiveScene` with an IPython shell attached
- `ManimCheckpointPaste` / `checkpoint_paste` sends selected code into the running shell
- Error output showing `Cell In[N]` style comes from IPython — it is NOT a Jupyter notebook

**Common gotcha:** If `Circle` etc. are `NameError`, `from manimlib import *` hasn't run yet. Fix: re-run the full scene via `ManimRunScene`.

**LaTeX:** User has MacTeX installed for `Tex`/`TexText`.

---

## Critical: MathTex Does Not Exist in ManimGL

**`MathTex` does not exist in ManimGL.** Use `Tex` instead.

- `MathTex` is a community fork class — heavily documented online, so LLMs suggest it confidently
- Nothing at import time warns you — it only fails at runtime when instantiated
- `from manimlib import *` succeeds fine; the error only appears when the object is created

**Correct classes:**
| Class | Use for |
|-------|---------|
| `Tex` | LaTeX math — replaces `MathTex` |
| `TexText` | LaTeX with text mode |
| `MarkupText` | Pango markup |
| `Text` | Plain text |

**Verify any class exists:**
```bash
/Users/skim/.pyenv/versions/3.11.14/bin/python3 -c "from manimlib import *; print([x for x in dir() if 'tex' in x.lower()])"
```

---

## Architecture Overview

### Scene
Subclass `Scene` (render to file) or `InteractiveScene` (live development with IPython):

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        self.clear()  # wipe previous objects when re-running
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

### Mobjects
All visual elements inherit `Mobject` → `VMobject` → specific shapes. Stored as NumPy vertex arrays, rendered via GPU shaders.

Core transforms: `shift()`, `scale()`, `rotate()`, `move_to()`, `next_to()`, `align_to()`
Core styling: `set_color()`, `set_fill()`, `set_stroke()`, `set_opacity()`

**Key types:**
| Class | Description |
|-------|-------------|
| `Circle`, `Arc`, `Dot` | Circular geometry |
| `GlowDot`, `TrueDot` | GPU-rendered dots with glow effects |
| `Line`, `Arrow`, `DashedLine`, `Vector` | Linear geometry |
| `Rectangle`, `Square`, `Polygon` | Polygons |
| `Tex`, `TexText`, `Text` | Text/math |
| `Axes`, `ThreeDAxes`, `NumberLine`, `NumberPlane` | Coordinate systems |
| `ComplexPlane` | Complex number plane |
| `ParametricCurve`, `FunctionGraph` | Plotted functions |
| `Sphere`, `ParametricSurface`, `SurfaceMesh` | 3D surfaces |
| `VectorField`, `StreamLines` | Vector field visualizations |
| `ValueTracker`, `ComplexValueTracker` | Animatable scalars (invisible) |
| `TracingTail` | Fading trail behind a moving mobject |
| `DecimalNumber`, `Integer` | Animatable number displays |
| `SurroundingRectangle`, `Brace` | Annotation shapes |
| `VGroup` | Group of VMobjects |
| `Group` | Group of any Mobjects (use for non-VMobjects like GlowDot, ImageMobject) |
| `ImageMobject` | Raster images |

### Rendering Pipeline
```
construct() → add/animate Mobjects → interpolate per frame
→ NumPy arrays → GPU via ModernGL → GLSL shaders → FFmpeg → .mp4
```

---

## Coordinate System

- Scene space: ~14 units wide × ~8 units tall (1080p)
- Origin at center
- Directions: `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL`, `UR`, `DL`, `DR`
- 3D: `OUT`, `IN` (Z-axis)
- Colors: `RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`, `BLACK`, `GREY`, etc.
- Math constants: `PI`, `TAU`, `DEG`

---

## CLI

```bash
manimgl my_scene.py MyScene          # interactive preview
manimgl my_scene.py MyScene -w       # write to video file
manimgl my_scene.py MyScene -l       # low quality
manimgl my_scene.py MyScene -o       # open on finish
manimgl my_scene.py MyScene -n 5     # start at animation #5
```

---

## Repository Structure (for targeted fetches)

```
manimlib/
├── animation/        creation.py, fading.py, transform.py, composition.py, indication.py ...
├── mobject/
│   ├── geometry/     arc.py, line.py, polygram.py, shape_matchers.py
│   ├── svg_mobject/  tex_mobject.py, string_mobject.py
│   ├── functions/    parametric_curve.py, implicit_curve.py
│   ├── types/        vectorized_mobject.py, dot_cloud.py, image_mobject.py
│   ├── coordinate_systems.py
│   ├── number_line.py
│   └── value_tracker.py
├── scene/            scene.py, interactive_scene.py
├── camera/           camera_frame.py
├── utils/            rate_functions.py, space_ops.py, bezier.py ...
└── constants.py
```
