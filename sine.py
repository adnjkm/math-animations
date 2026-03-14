from manimlib import *


class SinDerivation(InteractiveScene):
    def construct(self):
        self.clear()

        R = 1.8  # unit circle radius
        circle_center = np.array([-4.2, -0.3, 0])
        graph_center = np.array([2.5, -0.3, 0])

        # === 1. Write f(x) = sin(x) ===
        formula = Tex(r"f(x) = \sin(x)")
        formula.scale(1.4)
        self.play(Write(formula))
        self.wait(0.5)
        self.play(formula.animate.scale(0.6).to_edge(UP))

        # === 2. Unit circle ===
        circ_axes = Axes(
            x_range=(-1, 1, 1),
            y_range=(-1, 1, 1),
            width=2 * R,
            height=2 * R,
        ).move_to(circle_center)

        unit_circle = Circle(radius=R).move_to(circle_center)
        self.play(ShowCreation(circ_axes), ShowCreation(unit_circle))

        # === 3. Angle geometry ===
        theta = ValueTracker(PI / 3)

        def tip():
            t = theta.get_value()
            return circle_center + R * np.array([np.cos(t), np.sin(t), 0])

        def foot():  # base of the vertical drop
            t = theta.get_value()
            return circle_center + np.array([R * np.cos(t), 0, 0])

        radius_line = always_redraw(lambda: Line(circle_center, tip(), color=WHITE))
        opp_line = always_redraw(lambda: Line(foot(), tip(), color=RED, stroke_width=3))
        adj_line = always_redraw(lambda: Line(circle_center, foot(), color=GREEN, stroke_width=3))
        angle_arc = always_redraw(lambda: Arc(
            radius=0.4,
            start_angle=0,
            angle=max(theta.get_value(), 0.001),
            arc_center=circle_center,
            color=YELLOW,
        ))
        circle_dot = always_redraw(lambda: Dot(tip(), color=YELLOW, radius=0.09))

        theta_label = Tex(r"\theta", color=YELLOW)
        theta_label.scale(0.8)
        theta_label.add_updater(lambda m: m.move_to(
            circle_center + 0.7 * np.array([
                np.cos(theta.get_value() / 2),
                np.sin(theta.get_value() / 2),
                0,
            ])
        ))

        self.play(
            ShowCreation(radius_line),
            ShowCreation(angle_arc),
            FadeIn(circle_dot),
            Write(theta_label),
        )
        self.play(ShowCreation(opp_line), ShowCreation(adj_line))

        sin_label = Tex(r"\sin\theta = \frac{\text{opp}}{\text{hyp}} = y")
        sin_label.scale(0.65)
        sin_label.next_to(unit_circle, DOWN, buff=0.25)
        self.play(Write(sin_label))
        self.wait(0.5)

        # === 4. Graph axes ===
        graph_axes = Axes(
            x_range=(0, TAU, PI / 2),
            y_range=(-1.5, 1.5, 0.5),
            width=7,
            height=3.5,
        ).move_to(graph_center)

        pi_labels = VGroup(*[
            Tex(tex).scale(0.5).next_to(graph_axes.c2p(val, 0), DOWN, buff=0.15)
            for tex, val in [
                (r"\frac{\pi}{2}", PI / 2),
                (r"\pi", PI),
                (r"\frac{3\pi}{2}", 3 * PI / 2),
                (r"2\pi", TAU),
            ]
        ])

        self.play(ShowCreation(graph_axes), Write(pi_labels))

        # === 5. Trace the sine curve ===
        self.play(theta.animate.set_value(0.0001), run_time=0.5)

        graph_dot = always_redraw(lambda: Dot(
            graph_axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=YELLOW,
            radius=0.09,
        ))

        # Horizontal dashed line showing the y-value mapping across
        connect_line = always_redraw(lambda: DashedLine(
            tip(),
            graph_axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=RED,
            stroke_width=1.5,
        ))

        # Curve builds up as theta increases
        sin_curve = always_redraw(lambda: ParametricCurve(
            lambda t: graph_axes.c2p(t, np.sin(t)),
            t_range=[0, max(theta.get_value(), 0.001), 0.01],
            color=BLUE,
            stroke_width=3,
        ))

        self.add(sin_curve, graph_dot, connect_line)
        self.play(theta.animate.set_value(TAU), run_time=8, rate_func=linear)
        self.wait()
