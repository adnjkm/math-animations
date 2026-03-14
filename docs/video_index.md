# 3b1b/videos — Scene Index

Scan this to find real production examples similar to what you're building. Each entry has a one-line summary and key visualizations used. Fetch code at: `https://raw.githubusercontent.com/3b1b/videos/master/<path>`

---

## 2015

**`_2015/matrix_as_transform_2d.py`** — 2D matrix transformations visualized as warping the plane.
- Grid distortion, column vectors as basis images

**`_2015/eulers_characteristic_formula.py`** — Euler's V - E + F = 2 for polyhedra.
- 3D solids, face/edge/vertex counting animations

**`_2015/moser_intro.py` / `moser_main.py`** — Early Moser circle problem (revisited in 2023).
- Circle with chord intersections, combinatorial counting

---

## 2016

**`_2016/eola/`** — Essence of Linear Algebra series (vectors, matrices, determinants, eigenvectors).
- Vector field transformations, basis changes, 2D/3D linear maps, dot products, cross products

**`_2016/zeta.py`** — Riemann zeta function and analytic continuation.
- Complex plane mapping, color-coded domain coloring, strip transformations

---

## 2017

**`_2017/eoc/`** — Essence of Calculus series (derivatives, integrals, chain rule, Taylor series).
- Slope animations, area-under-curve, limit definitions, graph tangent lines

**`_2017/nn/`** — How neural networks learn: backpropagation, gradient descent.
- Layered network diagrams, weight visualizations, training animations

---

## 2018

**`_2018/fourier.py`** — Fourier transforms: winding a signal around a circle to extract frequencies.
- Rotating phasors, center-of-mass tracing, frequency decomposition bars

**`_2018/div_curl.py`** — Divergence and curl of vector fields.
- Animated vector fields, fluid flow, source/sink visualization

**`_2018/quaternions.py`** / **`_2018/quat3d.py`** — Quaternion rotation in 4D projected to 3D.
- 3D sphere rotation, stereographic projection, animated 4D paths

**`_2018/uncertainty.py`** — Uncertainty principle (signal processing version).
- Gaussian wave packets, Fourier pairs, frequency vs. time trade-off

---

## 2019

**`_2019/diffyq/`** — Differential equations series: pendulums, phase space, Fourier.
- Phase portraits, vector field flow, ODE trajectory tracing

**`_2019/bayes/`** — Bayes' theorem through visual probability areas.
- Rectangle partitioning, probability tree diagrams

**`_2019/clacks/`** — Colliding blocks computing digits of pi.
- Two blocks with elastic collisions, trajectory angle counting

---

## 2020

**`_2020/hamming.py`** — Hamming error-correcting codes explained visually.
- Binary grid with highlighted parity bits, XOR visualization

**`_2020/beta/`** — Beta distribution and Bayesian inference for estimating proportions.
- PDF/CDF animations, distribution updates with data

**`_2020/covid.py`** — SIR epidemic model animated.
- Dot population simulation, S/I/R curve graphs, exponential growth

---

## 2021

**`_2021/newton_fractal.py`** — Newton's method fractals in the complex plane.
- GPU-rendered fractal (custom `Mobject` subclass), complex iteration coloring, root basins

**`_2021/holomorphic_dynamics.py`** — Mandelbrot and Julia sets.
- GPU-rendered Mandelbrot/Julia fractals, parameter space exploration, animated Julia parameter sweep

**`_2021/matrix_exp.py`** — Matrix exponentiation, ODEs, and quantum mechanics.
- Matrix power sequences, rotation matrix continuum, differential equation solutions

**`_2021/shadows.py`** — Why shadow area of a convex solid equals 1/4 surface area.
- 3D solids with real-time shadow projection, `ThreeDScene` with light source, surface area gloss/material

**`_2021/quick_eigen.py`** — Quick eigenvalue trick for 2×2 matrices.
- Characteristic polynomial visualization, eigenvalue formulas

---

## 2022

**`_2022/borwein/main.py`** — Borwein integrals: why a pattern of sinc integrals mysteriously breaks.
- Sine function graphs, moving average convolution, Fourier diagram, reciprocal sum convergence

**`_2022/convolutions/discrete.py`** — Convolution of discrete distributions via dice rolling.
- Bar chart histograms (`ChartBars`), sliding/aligning two dice rows, polynomial multiplication grid

**`_2022/galois/groups.py`** — Group theory and Galois theory through symmetries.
- Symmetry operations on polygons and flowers, group tables, permutation diagrams

**`_2022/quintic/cubic.py`** — Why the quintic has no formula: cubic/quartic solutions, Galois groups.
- Root locus in complex plane, permutation group diagrams, polynomial coefficient relationships

**`_2022/infinity/`** — Different sizes of infinity, Cantor's diagonal argument.
- Bijection diagrams, countable vs uncountable sets, diagonal construction

**`_2022/wordle/scenes.py`** — Information theory and entropy through Wordle.
- Probability distributions as bars, entropy formula, letter frequency grid

**`_2022/piano/fourier_animations.py`** — Fourier decomposition of musical sounds.
- Waveform stacking, frequency component separation, 3D basis vector analogy

**`_2022/zeta/`** — Riemann zeta function, prime connection, analytic continuation.
- Complex function mapping, zero locations, Euler product visualization

**`_2022/visual_proofs/lies.py`** — "Proof" that π = 4 and other visual fallacies.
- Circle/sphere approximations with step functions, limit pitfalls, surface area comparisons

---

## 2023

**`_2023/clt/main.py`** — Central Limit Theorem: why sums of random variables become Gaussian.
- Die distribution bar charts (`ChartBars` + `DieFace`), convolution as distribution spreading, Gaussian overlay

**`_2023/convolutions2/continuous.py`** — Continuous convolution: sliding window integral interpretation.
- Continuous probability density animations, convolution as sliding/flipping, Gaussian self-convolution

**`_2023/gauss_int/integral.py`** — Gaussian integral equals √π via 3D polar coordinates.
- 3D cylinder and Cartesian slice decomposition (`ThreeDScene`), volume-under-surface animations

**`_2023/moser_reboot/main.py`** — Moser's circle problem: why 1,2,4,8,16,31 breaks the pattern.
- Circle with chord intersections, combinatorial counting labels, Pascal's triangle

**`_2023/optics_puzzles/bending_waves.py`** — Snell's law derived from wave physics.
- Wave fronts bending at medium boundary (`TimeVaryingVectorField`), phase speed visualization, Fermat's principle

---

## 2024

**`_2024/antp/main.py`** — Analytic number theory: prime number theorem, Sieve of Eratosthenes.
- Prime density histograms, sieve animation, logarithmic distribution graphs, Dirichlet series

**`_2024/linalg/eigenlecture.py`** — Eigenvalues, eigenvectors, diagonalization, Fibonacci closed form.
- Matrix-vector equations with colored entries (`t2c`), vector field + stream lines, change-of-basis diagrams

**`_2024/transformers/attention.py`** — Attention mechanism in transformers.
- Word embedding vectors (`NumericEmbedding`), attention arrows between tokens, matrix-vector products animated step by step

**`_2024/transformers/embedding.py`** — Word embeddings and token representation.
- High-dimensional vector visualization, word-to-vector mapping, semantic direction arrows

**`_2024/transformers/mlp.py`** — MLP layers in transformers: weights, biases, activation functions.
- Layered grid of numbers, weighted sum animations, ReLU activation visualization

**`_2024/holograms/diffraction.py`** — Holograms via wave diffraction and zone plates.
- Wave interference patterns, diffraction grating animations, complex wave superposition

**`_2024/inscribed_rect/loops.py`** — Inscribed rectangle theorem proved via topology.
- Möbius strip / Klein bottle construction in 3D, loop-to-surface mapping, continuous deformation

**`_2024/manim_demo/lorenz.py`** — Lorenz attractor: chaos and sensitivity to initial conditions.
- `ThreeDAxes` + ODE integration via scipy, `VMobject.set_points_smoothly()` for trajectories, `TracingTail`, ambient camera rotation, `fix_in_frame()` equation label

---

## 2025

**`_2025/laplace/derivatives.py`** + **`main_equations.py`** + **`exponentials.py`** + **`integration.py`** — Laplace transform series.
- `ComplexPlane`, `ComplexValueTracker`, pole locations in s-plane, `fix_in_frame()` time-domain graphs alongside 3D s-plane, forced oscillator animation

**`_2025/spheres/volumes.py`** — Volume and surface area of n-dimensional spheres.
- `Sphere` with `always_sort_to_camera`, `SurfaceMesh`, `set_clip_plane()` to animate cross-sections, inner sphere shells

**`_2025/grover/state_vectors.py`** — Grover's quantum search algorithm via state vector geometry.
- Quantum state amplitude bars, rotation in Hilbert space, qubit visualization

**`_2025/cosmic_distance/planets.py`** — Cosmic distance ladder: from Earth's radius to stellar distances.
- Orbital diagrams, parallax geometry, planet scale comparisons, Kepler's laws animation

**`_2025/colliding_blocks_v2/blocks.py`** — Colliding blocks encoding digits of pi in collision count.
- Two-block elastic collision simulation, phase space trajectory, angle counting

**`_2025/zeta/play.py`** — Riemann zeta function: sum formulas and log-derivative connection to primes.
- Complex sum visualization, prime-connected series

---

## 2026

**`_2026/hairy_ball/spheres.py`** — Hairy ball theorem: every continuous vector field on a sphere has a zero.
- `StreamLines` on sphere surface, `StereographicProjection`, flow line animations, null point detection, `SurfaceMesh` + vector field

---

## Utility / Reusable Constructs

**`once_useful_constructs/`** — Reusable scene types from older videos (may use older API):
- `complex_transformation_scene.py` — complex function domain coloring
- `vector_space_scene.py` — vector space with basis, span, linear combinations
- `sample_space_scene.py` — probability sample space rectangles
- `graph_scene.py` — older graph plotting utilities (pre-Axes)

**`custom/`** — Shared assets across all videos:
- `backdrops.py` — colored background scenes
- `drawings.py` — reusable drawing elements
- `characters/pi_creature` — the Pi creature character and animations
