# Past Errors & How to Avoid Them

Read this before writing new ManimGL code. Each entry has: what broke, why it happened, and the mental check to avoid repeating it.

---

## 1. Using `MathTex` instead of `Tex`

**Error:**
```
NameError: name 'MathTex' is not defined
```

**What happened:**
`MathTex` is the LaTeX class in `manim-community` (the popular fork). It is heavily documented online and appears far more in LLM training data than the original ManimGL equivalent. Claude confidently suggested `MathTex` because it's so common in general Manim content.

In ManimGL, `from manimlib import *` succeeds fine — `MathTex` doesn't error at import. The crash only happens at runtime when the object is actually instantiated, making it easy to miss.

**Root cause of the wrong diagnosis:**
Claude initially suspected a missing import or MacTeX issue rather than a nonexistent class — because `MathTex` *feels* like it should exist. The correct diagnosis required checking what's actually exported by `manimlib`.

**The fix:**
Use `Tex` for all LaTeX math in ManimGL. `MathTex` does not exist here.

**Mental check before using any class:**
> "Is this class name from a community-fork tutorial or Stack Overflow answer? If so, verify it exists in ManimGL before using it."

Verify with:
```bash
/Users/skim/.pyenv/versions/3.11.14/bin/python3 -c "from manimlib import *; print([x for x in dir() if 'keyword' in x.lower()])"
```

Or fetch `https://raw.githubusercontent.com/3b1b/manim/master/manimlib/__init__.py` to see all exports.

**Never assume community-fork class names carry over to ManimGL.** Key differences:
| ManimGL (correct) | manim-community (wrong here) |
|-------------------|------------------------------|
| `Tex` | `MathTex` |
| `ShowCreation` | `Create` |
| `InteractiveScene` | no equivalent |

---

## 2. `ParametricCurve` with only 2 values in `t_range`

**Error:**
```
ValueError: not enough values to unpack (expected 3, got 2)
```

**What happened:**
`ParametricCurve` in ManimGL requires `t_range` to have exactly 3 values: `[min, max, step]`. Passing only `[min, max]` crashes at runtime.

```python
# WRONG
ParametricCurve(func, t_range=[0, TAU])

# CORRECT
ParametricCurve(func, t_range=[0, TAU, 0.01])
```

**Why it's easy to miss:**
The step value feels optional (many plotting APIs infer it). Nothing in the function signature makes the requirement obvious. It only crashes at runtime, not at definition time.

**Additional gotcha:**
When using `always_redraw` with a growing curve (e.g. tracing as a `ValueTracker` increases), the `t_range` max can reach zero at the start. Guard against this:

```python
sin_curve = always_redraw(lambda: ParametricCurve(
    lambda t: axes.c2p(t, np.sin(t)),
    t_range=[0, max(theta.get_value(), 0.001), 0.01],  # never zero-length
    color=BLUE,
))
```

**Mental check:**
> "Does my `t_range` have exactly 3 values? Is there any case where max - min could be zero or negative?"

---

## 3. Assuming the user is running a Jupyter notebook

**Error:** No crash — just completely wrong mental model, leading to bad debugging advice.

**What happened:**
IPython (used inside the Sublime Text + Terminus workflow) formats errors with `Cell In[N], line X:` — the same format as Jupyter notebook errors. Claude assumed Jupyter and gave irrelevant advice about notebook cell order and kernel restarts.

**The actual workflow:**
- User runs scenes from **Sublime Text** via `ManimRunScene` command
- This sends `manimgl <file>.py <ClassName>` to a **Terminus** terminal tab
- That boots a live `InteractiveScene` with an **IPython shell** attached
- `checkpoint_paste` sends selected code from the editor into that running shell
- `Cell In[N]` in error output comes from IPython, NOT Jupyter

**Mental check:**
> "If I see `Cell In[N]` in an error, that's IPython formatting inside Terminus — not a notebook. Don't suggest notebook-related fixes. The code runs from Sublime Text."

**Common gotcha:** If `Circle`, `Tex`, etc. are `NameError`, it means `from manimlib import *` hasn't run in the current shell session. Fix: re-run the full scene via `ManimRunScene` (cursor inside the class body) to boot a fresh session.

---

## 4. Passing a `Tex` object to `get_x_axis_label` / `get_y_axis_label`

**Error:**
```
TypeError: sequence item 0: expected str instance, Tex found
```

**What happened:**
`axes.get_x_axis_label(Tex("x", font_size=18))` was called with a pre-built `Tex` object. Internally, `get_axis_label` does `label = Tex(label_tex)` — wrapping the argument in `Tex` itself. Passing a `Tex` object makes it call `Tex(Tex(...))`, which crashes.

**The fix:**
Pass a plain string:
```python
# WRONG
xl = axes.get_x_axis_label(Tex("x", font_size=18))

# CORRECT
xl = axes.get_x_axis_label("x")
```

To control font size, scale the returned label:
```python
xl = axes.get_x_axis_label("x")
xl.scale(0.7)
```

**Mental check:**
> "`get_x_axis_label` / `get_y_axis_label` take a **string**, not a Tex object — they build the Tex internally."

---

## General Rules to Avoid These Errors

1. **Always fetch from the ManimGL GitHub repo** when in doubt about an API — never assume community-fork docs apply: `https://raw.githubusercontent.com/3b1b/manim/master/manimlib/__init__.py`

2. **Verify any class before using it** — especially if it came from an online tutorial, Stack Overflow, or a community-fork example.

3. **Check runtime-only errors carefully** — ManimGL imports succeed even for nonexistent classes. The error only appears when the object is instantiated.

4. **The user's environment is Sublime Text + Terminus + IPython** — not Jupyter, not a plain terminal, not VS Code.
