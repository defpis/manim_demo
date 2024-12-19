from manim import *


def calc(x):
    return (10 - 2 * x) * (10 - 2 * x) * x


x_1 = [[i, calc(i)] for i in np.arange(0.0, 6.0, 1.0)]
x_2 = [[i, calc(i)] for i in np.arange(0.0, 5.5, 0.5)]
x_3 = [[i, calc(i)] for i in np.arange(0.0, 5.1, 0.1)]

dot_size = 0.08


class CustomAnimation(Scene):
    def construct(self):

        table = Table(
            [[f"{p[0]}", f"{p[1]}"] for p in x_1],
            col_labels=[Text("x"), Text("y")],
            include_outer_lines=True,
            line_config={"stroke_width": 2},
        )
        table.scale(0.5)

        axes = NumberPlane(
            x_range=(0, 5, 1),
            y_range=(0, 100, 10),
            y_length=6,
            x_length=10,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        )
        axes.scale(0.8)

        g0 = VGroup(table, axes).arrange(RIGHT, buff=2)
        self.add(g0)

        h_dot = Dot(radius=dot_size, point=axes.c2p(0, 0), fill_color=RED)

        # -------- 虚线
        h_lines = always_redraw(lambda: axes.get_lines_to_point(h_dot.get_center()))
        self.add(h_lines)
        # -------- 虚线

        # --------  高亮块
        start_row = 2
        cell = table.get_cell((start_row, 1))
        step = cell.get_top()[1] - cell.get_bottom()[1]

        h_rect = BackgroundRectangle(
            VGroup(table.get_cell((start_row, 1)), table.get_cell((start_row, 2))),
            fill_color=GREEN,
        )
        # --------  高亮块

        self.play([FadeIn(h_dot, scale=0.5), Create(h_rect)])

        dots = []
        for i, p in enumerate(x_1):
            _pos = axes.c2p(p[0], p[1])

            if i != 0:
                self.play(
                    [
                        h_rect.animate.shift(DOWN * step),
                        h_dot.animate.move_to(_pos),
                    ]
                )
                self.wait()

            _dot = Dot(radius=dot_size, point=_pos, fill_color=WHITE)
            self.add(_dot)
            dots.append(_dot)

        self.remove(h_dot)
        self.remove(h_lines)
        self.remove(h_rect)

        lines = []
        for i in range(0, len(dots) - 1):
            src = dots[i]
            dst = dots[i + 1]
            _line = Line(
                src.get_center(), dst.get_center(), stroke_width=2, color=WHITE
            )
            self.play(Create(_line))
            lines.append(_line)

        self.wait()

        self.play(FadeOut(table))
        self.wait()

        g1 = VGroup(axes, *dots, *lines)

        x_step = ValueTracker(1)
        show_numbers = ValueTracker(True)

        def create_group(pos):
            axes = NumberPlane(
                x_range=(0, 5, x_step.get_value()),
                y_range=(0, 100, 10),
                y_length=6,
                x_length=10,
                tips=False,
                axis_config={
                    "include_numbers": show_numbers.get_value(),
                    "font_size": 20,
                },
            )

            dots = []
            for i, p in enumerate(pos):
                _pos = axes.c2p(p[0], p[1])
                _dot = Dot(radius=dot_size, point=_pos, fill_color=WHITE)
                dots.append(_dot)

            lines = []
            for i in range(0, len(dots) - 1):
                src = dots[i]
                dst = dots[i + 1]
                _line = Line(
                    src.get_center(), dst.get_center(), stroke_width=2, color=WHITE
                )
                lines.append(_line)

            return VGroup(axes, *dots, *lines)

        # ---------------
        g2 = always_redraw(lambda: create_group(x_1))

        self.play(ReplacementTransform(g1, g2))
        self.wait()

        show_numbers.set_value(False)
        self.play(x_step.animate.set_value(0.5))
        self.wait()
        self.play(show_numbers.animate.set_value(True))
        self.wait()

        axes = g2[0]
        dots = list(g2[1 : 1 + len(x_1)])
        lines = list(g2[1 + len(x_1) :])

        self.play(FadeOut(*lines))
        self.wait()

        h_dot = Dot(radius=dot_size, point=axes.c2p(0, 0), fill_color=RED)
        self.play([FadeIn(h_dot, scale=0.5)])

        h_lines = always_redraw(lambda: axes.get_lines_to_point(h_dot.get_center()))
        self.add(h_lines)

        _dots = []
        for i, p in enumerate(x_2):
            _pos = axes.c2p(p[0], p[1])

            if i != 0:
                self.play(h_dot.animate.move_to(_pos))
                self.wait()

            _dot = Dot(radius=dot_size, point=_pos, fill_color=WHITE)
            self.add(_dot)
            _dots.append(_dot)

        self.remove(h_dot)
        self.remove(h_lines)

        self.remove(*dots)
        dots = _dots

        lines = []
        for i in range(0, len(dots) - 1):
            src = dots[i]
            dst = dots[i + 1]
            _line = Line(
                src.get_center(), dst.get_center(), stroke_width=2, color=WHITE
            )
            self.play(Create(_line))
            lines.append(_line)
        # ---------------

        axes2 = always_redraw(
            lambda: NumberPlane(
                x_range=(0, 5, x_step.get_value()),
                y_range=(0, 100, 10),
                y_length=6,
                x_length=10,
                tips=False,
                axis_config={
                    "include_numbers": show_numbers.get_value(),
                    "font_size": 20,
                },
            )
        )

        self.play(ReplacementTransform(axes, axes2))
        self.wait()

        show_numbers.set_value(False)
        self.play(x_step.animate.set_value(0.1))
        self.wait()

        self.play(FadeOut(*lines))
        self.wait()

        h_dot = Dot(radius=dot_size, point=axes.c2p(0, 0), fill_color=RED)
        self.play([FadeIn(h_dot, scale=0.5)])

        h_lines = always_redraw(lambda: axes.get_lines_to_point(h_dot.get_center()))
        self.add(h_lines)

        _dots = []
        for i, p in enumerate(x_3):
            _pos = axes.c2p(p[0], p[1])

            if i != 0:
                self.play(h_dot.animate.move_to(_pos), run_time=0.1)

            _dot = Dot(radius=dot_size, point=_pos, fill_color=WHITE)
            self.add(_dot)
            _dots.append(_dot)

        self.remove(h_dot)
        self.remove(h_lines)

        self.remove(*dots)
        dots = _dots

        lines = []
        for i in range(0, len(dots) - 1):
            src = dots[i]
            dst = dots[i + 1]
            _line = Line(
                src.get_center(), dst.get_center(), stroke_width=2, color=WHITE
            )
            self.play(Create(_line), run_time=0.1)
            lines.append(_line)
        # ---------------

        self.play([FadeOut(*lines), FadeOut(*dots)])
        self.wait()

        curve = axes2.plot(lambda x: calc(x), color=YELLOW)
        self.play(Create(curve))
        self.wait()
