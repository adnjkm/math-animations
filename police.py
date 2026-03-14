from manimlib import *
import numpy as np


def make_bullet(width, height, color=WHITE):
    """Bullet silhouette: rectangular case + rounded semicircle tip."""
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


class PoliceScene(InteractiveScene):
    def construct(self):
        self.clear()

        # Defined here so checkpoint_paste always has it in scope
        def make_node(color, r=0.22):
            glow = Circle(radius=r * 2.0)
            glow.set_fill(color, opacity=0.10)
            glow.set_stroke(color, 1.0, opacity=0.30)
            core = Dot(radius=r, color=color)
            return VGroup(glow, core)

        # ─── Caliber definitions ────────────────────────────────────────────
        GD = {
            0: dict(name=".22 LR",   color=YELLOW_D, w=0.16, h=0.68),
            1: dict(name="9mm",      color=BLUE_B,   w=0.22, h=0.90),
            2: dict(name=".45 ACP",  color=RED_B,    w=0.30, h=1.08),
            3: dict(name=".308 Win", color=ORANGE,   w=0.27, h=1.40),
        }

        # 4×4 grid: 4 of each caliber, interleaved
        flat = [3, 1, 0, 2, 0, 2, 3, 1, 1, 3, 2, 0, 2, 0, 1, 3]

        # ─── Phase 1: Title + spread grid ──────────────────────────────────
        title = Text("Ballistic Evidence Analysis", font_size=38)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        bullets = VGroup(*[
            make_bullet(GD[g]["w"], GD[g]["h"], GD[g]["color"])
            for g in flat
        ])

        # Manual placement: wide column spacing prevents "pillar" look
        # Bullets scaled down for grid so there's clear space between them;
        # they scale back to full size during the sort phase.
        GRID_SCALE = 0.55
        cols = 4
        col_spacing = 1.9   # >> bullet width
        row_spacing = 1.3   # fits scaled bullet height with visible gap
        grid_cy = -0.25     # shift down slightly for title

        for idx, b in enumerate(bullets):
            row = idx // cols
            col = idx % cols
            x = (col - (cols - 1) / 2.0) * col_spacing
            y = grid_cy + ((cols - 1) / 2.0 - row) * row_spacing
            b.scale(GRID_SCALE)
            b.move_to(np.array([x, y, 0.0]))

        self.play(LaggedStart(
            *[FadeIn(b, shift=DOWN * 0.25) for b in bullets],
            lag_ratio=0.05, run_time=1.8,
        ))
        self.wait(0.5)

        # ─── Phase 2: Sort into 4 caliber groups ───────────────────────────
        gm = {g: [] for g in GD}
        for i, gid in enumerate(flat):
            gm[gid].append(i)

        # Build temp_groups from full-size bullets so layout positions
        # account for the proper (unscaled) bullet dimensions.
        temp_groups = []
        for gid in range(4):
            sample = make_bullet(GD[gid]["w"], GD[gid]["h"], GD[gid]["color"])
            tg = VGroup(*[sample.copy() for _ in gm[gid]])
            tg.arrange_in_grid(n_rows=2, n_cols=2, buff=0.28)
            temp_groups.append(tg)

        temp_all = VGroup(*temp_groups)
        temp_all.arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        temp_all.center().shift(DOWN * 0.25)

        for gid in range(4):
            for li, bi in enumerate(gm[gid]):
                bullets[bi].generate_target()
                bullets[bi].target.move_to(temp_groups[gid][li].get_center())
                bullets[bi].target.scale(1.0 / GRID_SCALE)  # restore full size

        self.play(LaggedStart(
            *[MoveToTarget(bullets[i]) for i in range(len(bullets))],
            lag_ratio=0.04, run_time=2.0,
        ))
        self.wait(0.3)

        # ─── Phase 3: Rounded circles + caliber labels ─────────────────────
        grp_vg = [VGroup(*[bullets[i] for i in gm[g]]) for g in range(4)]

        circles = VGroup()
        glabels = VGroup()
        for gid, grp in enumerate(grp_vg):
            color = GD[gid]["color"]
            ring = SurroundingRectangle(grp, buff=0.28, color=color)
            ring.round_corners(0.35)
            ring.set_stroke(color, 2)
            ring.set_fill(color, opacity=0.05)
            lbl = Text(GD[gid]["name"], font_size=21, color=color)
            lbl.next_to(ring, UP, buff=0.15)
            circles.add(ring)
            glabels.add(lbl)

        self.play(LaggedStart(*[ShowCreation(c) for c in circles], lag_ratio=0.15))
        self.play(LaggedStart(*[Write(l) for l in glabels], lag_ratio=0.15))
        self.wait(0.7)

        # ─── Phase 4: Select 9mm → machine → output ────────────────────────
        self.play(
            *[grp_vg[g].animate.set_opacity(0.1) for g in [0, 2, 3]],
            *[circles[g].animate.set_opacity(0.1) for g in [0, 2, 3]],
            *[glabels[g].animate.set_opacity(0.1) for g in [0, 2, 3]],
            run_time=0.5,
        )
        self.play(
            FadeOut(title),
            *[FadeOut(grp_vg[g]) for g in [0, 2, 3]],
            *[FadeOut(circles[g]) for g in [0, 2, 3]],
            *[FadeOut(glabels[g]) for g in [0, 2, 3]],
            run_time=0.4,
        )

        nm9 = VGroup(grp_vg[1], circles[1], glabels[1])
        self.play(nm9.animate.move_to(LEFT * 4.5 + DOWN * 0.2))

        # Machine box
        mach = Rectangle(width=3.0, height=2.2)
        mach.set_stroke(GREY_B, 2)
        mach.set_fill(GREY_E, opacity=0.55)
        mach.move_to(ORIGIN)
        mach_lbl = Text("Ballistic\nDatabase", font_size=20, color=GREY_A)
        mach_lbl.move_to(mach)
        h_lines = VGroup(*[
            Line(
                mach.get_left() + RIGHT * 0.2 + UP * dy,
                mach.get_right() + LEFT * 0.2 + UP * dy,
            ).set_stroke(GREY_C, 0.8)
            for dy in [-0.45, 0.0, 0.45]
        ])
        arr_in  = Arrow(LEFT * 2.9, mach.get_left(),   buff=0, stroke_width=3, color=GREY_B)
        arr_out = Arrow(mach.get_right(), RIGHT * 2.9, buff=0, stroke_width=3, color=BLUE_B)
        lbl_in  = Text("evidence in", font_size=13, color=GREY_C).next_to(arr_in,  UP, buff=0.06)
        lbl_out = Text("match out",   font_size=13, color=GREY_C).next_to(arr_out, UP, buff=0.06)

        self.play(
            FadeIn(mach), FadeIn(h_lines), Write(mach_lbl),
            GrowArrow(arr_in), GrowArrow(arr_out),
            Write(lbl_in), Write(lbl_out),
        )
        self.wait(0.2)

        self.play(
            grp_vg[1].animate.scale(0.5).move_to(mach.get_center()),
            circles[1].animate.scale(0.01).move_to(mach.get_center()),
            glabels[1].animate.scale(0.01).move_to(mach.get_center()),
            run_time=0.9,
        )
        self.remove(grp_vg[1], circles[1], glabels[1])
        self.play(mach.animate.set_fill(BLUE_E, opacity=0.4), run_time=0.25)
        self.play(mach.animate.set_fill(GREY_E, opacity=0.55), run_time=0.25)

        gun_text = Text("Glock 17", font_size=44, color=BLUE_B)
        gun_text.move_to(RIGHT * 4.8)
        self.play(Write(gun_text))
        self.wait(0.5)

        # ─── Phase 5: Business card ─────────────────────────────────────────
        self.play(*[FadeOut(m) for m in list(self.mobjects)])
        self.wait(0.2)

        # Card body
        card = Rectangle(width=10.5, height=5.2)
        card.set_stroke(BLUE_B, 2.5)
        card.set_fill(GREY_E, opacity=0.93)
        card.move_to(UP * 0.9)

        # Header strip along top of card
        header_strip = Rectangle(width=10.5, height=0.85)
        header_strip.set_stroke(width=0)
        header_strip.set_fill(BLUE_E, opacity=0.40)
        header_strip.align_to(card, UP)

        header_txt = Text("BALLISTIC EVIDENCE FILE", font_size=16, color=GREY_A)
        header_txt.move_to(header_strip).shift(LEFT * 2.8)
        case_txt = Text("CASE #A-2847", font_size=13, color=GREY_C)
        case_txt.move_to(header_strip).shift(RIGHT * 3.8)

        # Gun info block
        gun_title = Text("FIREARM:  GLOCK 17", font_size=28, color=WHITE)
        gun_specs = VGroup(
            Text("Caliber:   9 × 19mm Parabellum",     font_size=16, color=GREY_B),
            Text("Serial:    GHK-38291-C",              font_size=16, color=GREY_B),
            Text("Rifling:   Hexagonal, right-hand",    font_size=16, color=GREY_B),
        )
        gun_specs.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        gun_block = VGroup(gun_title, gun_specs)
        gun_block.arrange(DOWN, buff=0.22, aligned_edge=LEFT)

        # Position gun_block: y just below header, x left-aligned with margin
        gun_block.next_to(header_strip, DOWN, buff=0.3)
        gun_block.align_to(card.get_left() + RIGHT * 0.55, LEFT)

        # Divider
        h_div = Line(
            card.get_left() + RIGHT * 0.4,
            card.get_right() + LEFT * 0.4,
        ).set_stroke(GREY_D, 1)
        h_div.next_to(gun_block, DOWN, buff=0.3)

        # Owner section
        owner_hdr = Text("REGISTERED OWNER", font_size=13, color=GREY_C)
        owner_hdr.next_to(h_div, DOWN, buff=0.22)
        owner_hdr.align_to(gun_block, LEFT)

        searching = Text("● SEARCHING DATABASE...", font_size=20, color=YELLOW)
        searching.next_to(owner_hdr, DOWN, buff=0.2)
        searching.align_to(owner_hdr, LEFT)

        # Animate card building up
        self.play(FadeIn(VGroup(card, header_strip, header_txt, case_txt)))
        self.play(
            Write(gun_title),
            LaggedStartMap(FadeIn, gun_specs, lag_ratio=0.15),
        )
        self.play(ShowCreation(h_div), Write(owner_hdr))
        self.play(Write(searching))
        self.wait(0.3)

        # ─── Phase 6: Horizontal name tape scrolls below card ──────────────
        tape_y = card.get_bottom()[1] - 0.55

        tape_strip = Rectangle(width=FRAME_WIDTH + 1, height=0.72)
        tape_strip.set_stroke(GREY_D, 1)
        tape_strip.set_fill(GREY_D, opacity=0.18)
        tape_strip.move_to(np.array([0.0, tape_y, 0.0]))
        self.play(FadeIn(tape_strip))

        names_raw = [
            "Adams, R.", "Alvarez, M.", "Barnes, K.", "Brewer, D.",
            "Carter, D.", "Chen, W.", "Collins, A.", "Davis, A.",
            "Evans, Marcus J.",          # ← MATCH  idx=8
            "Fletcher, A.", "Garcia, L.", "Greene, P.", "Harris, J.",
            "Holmes, T.", "Jackson, K.", "Jenkins, R.", "Kim, D.",
            "Lopez, C.", "Martin, T.", "Mills, C.", "Murphy, B.",
        ]
        MATCH_IDX = 8

        tape = VGroup(*[
            Text(n, font_size=24, color=(TEAL if i == MATCH_IDX else GREY_B))
            for i, n in enumerate(names_raw)
        ])
        tape.arrange(RIGHT, buff=1.1)
        tape.move_to(np.array([0.0, tape_y, 0.0]))

        # Start tape off-screen right, scroll left until match is centered
        tape.align_to(RIGHT_SIDE, LEFT)
        self.add(tape)

        shift_amt = tape[MATCH_IDX].get_center()[0]   # match starts this far right of 0
        self.play(
            tape.animate.shift(LEFT * shift_amt),
            run_time=4.0, rate_func=linear,
        )

        # Blink match name
        match_tape = tape[MATCH_IDX]
        for _ in range(3):
            self.play(match_tape.animate.set_color(YELLOW), run_time=0.12)
            self.play(match_tape.animate.set_color(TEAL),   run_time=0.12)

        # Reveal owner info on card (replace "searching")
        self.play(FadeOut(searching))

        owner_info = VGroup(
            Text("EVANS, Marcus J.",                              font_size=24, color=TEAL),
            Text("DOB:      March 14, 1989",                      font_size=15, color=GREY_A),
            Text("Address:  2847 Meridian Ave, Chicago IL",       font_size=15, color=GREY_A),
            Text("Priors:   Assault (2018)  ·  Firearms (2020)", font_size=15, color=GREY_A),
        )
        owner_info.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        owner_info.next_to(owner_hdr, DOWN, buff=0.2)
        owner_info.align_to(owner_hdr, LEFT)

        self.play(LaggedStartMap(FadeIn, owner_info, lag_ratio=0.15))
        self.wait(0.4)

        confirmed = Text("MATCH CONFIRMED", font_size=20, color=TEAL)
        confirmed.to_corner(DR, buff=0.45)
        self.play(Write(confirmed))
        self.wait(0.8)

        # ─── Phase 7: Gang network graph ───────────────────────────────────
        self.play(*[FadeOut(m) for m in list(self.mobjects)])
        self.wait(0.2)

        net_title = Text("Network Analysis — Identified Connections", font_size=30)
        net_title.to_edge(UP, buff=0.4)
        self.play(Write(net_title))

        NP = {
            "Evans":  np.array([ 0.0,  0.2, 0.0]),
            "Torres": np.array([-2.8,  1.8, 0.0]),
            "Santos": np.array([ 2.8,  1.8, 0.0]),
            "Reyes":  np.array([-2.8, -1.6, 0.0]),
            "Webb":   np.array([ 2.8, -1.6, 0.0]),
            "Kim":    np.array([ 0.0, -3.2, 0.0]),
        }
        NC = {
            "Evans":  BLUE_B,
            "Torres": RED_B, "Santos": RED_B,
            "Reyes":  RED_B, "Webb":   RED_B, "Kim": RED_B,
        }

        nodes = {}
        node_labels = {}
        for name, pos in NP.items():
            node = make_node(NC[name], r=0.28 if name == "Evans" else 0.20)
            node.move_to(pos)
            nodes[name] = node
            lbl = Text(name, font_size=17, color=NC[name])
            lbl.next_to(node, UP, buff=0.1)
            node_labels[name] = lbl

        id_lbl = Text("Marcus J. Evans", font_size=13, color=GREY_B)
        id_lbl.next_to(nodes["Evans"], DOWN, buff=0.1)

        self.play(FadeIn(nodes["Evans"]), Write(node_labels["Evans"]))
        self.play(Write(id_lbl))
        self.wait(0.3)

        # Reveal connections + nodes progressively
        reveal_steps = [
            ("Evans", "Torres", ["Torres"]),
            ("Evans", "Santos", ["Santos"]),
            ("Evans", "Reyes",  ["Reyes"]),
            ("Evans", "Webb",   ["Webb"]),
            ("Torres", "Reyes", []),
            ("Santos", "Webb",  []),
            ("Reyes",  "Kim",   ["Kim"]),
            ("Webb",   "Kim",   []),
        ]
        for a, b, new_nodes in reveal_steps:
            edge = Line(NP[a], NP[b]).set_stroke(GREY_C, 1.5, opacity=0.5)
            anims = [ShowCreation(edge)]
            for n in new_nodes:
                anims += [FadeIn(nodes[n]), Write(node_labels[n])]
            self.play(*anims, run_time=0.55)

        self.wait(0.5)

        # Apprehend suspects — each dims to grey
        for name in ["Torres", "Reyes", "Kim", "Santos", "Webb"]:
            flash = SurroundingRectangle(nodes[name], buff=0.1, color=RED)
            self.play(ShowCreation(flash), run_time=0.2)
            self.play(
                nodes[name].animate.set_color(GREY_C),
                node_labels[name].animate.set_color(GREY_C),
                FadeOut(flash),
                run_time=0.35,
            )

        self.wait(0.3)
        final = Text("5 suspects apprehended", font_size=26, color=GREEN)
        final.to_edge(DOWN, buff=0.5)
        self.play(Write(final))
        self.wait(2.0)
