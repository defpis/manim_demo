from manim import *

pos = [[0, 0], [1, 64], [2, 69], [3, 74], [4, 20], [5, 0]]


class CustomAnimation(Scene):
    def construct(self):

        table = Table(
            [[f"{p[0]}", f"{p[1]}"] for p in pos],
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

        group = VGroup(table, axes).arrange(RIGHT, buff=2)
        self.add(group)

        dot = Dot(point=axes.c2p(0, 0), fill_color=RED)

        # -------- 虚线
        # def get_dash_line(index):
        #     def make():
        #         p = dot.get_center()
        #         o = axes.c2p(0, 0)
        #         o[index] = p[index]
        #         return DashedLine(o, p, stroke_width=2, color=RED)

        #     return always_redraw(make)

        # h_line = get_dash_line(0)
        # v_line = get_dash_line(1)
        # self.add(h_line)
        # self.add(v_line)

        lines = always_redraw(lambda: axes.get_lines_to_point(dot.get_center()))
        self.add(lines)
        # -------- 虚线

        # --------  高亮块
        start_row = 2
        cell = table.get_cell((start_row, 1))
        step = cell.get_top()[1] - cell.get_bottom()[1]

        highlight = BackgroundRectangle(
            VGroup(table.get_cell((start_row, 1)), table.get_cell((start_row, 2))),
            fill_color=GREEN,
        )
        # --------  高亮块

        self.play([FadeIn(dot, scale=0.5), Create(highlight)])

        dots = []
        for i, p in enumerate(pos):
            _pos = axes.c2p(p[0], p[1])

            if i != 0:
                self.play(
                    [
                        highlight.animate.shift(DOWN * step),
                        dot.animate.move_to(_pos),
                    ]
                )
                self.wait()

            _dot = Dot(point=_pos, fill_color=WHITE)
            self.add(_dot)
            dots.append(_dot)

        self.remove(dot)
        self.remove(lines)
        self.remove(highlight)

        for i in range(0, len(dots) - 1):
            src = dots[i]
            dst = dots[i + 1]
            line = Line(src.get_center(), dst.get_center(), stroke_width=2, color=WHITE)
            self.play(Create(line))

        self.wait(2)

        group.remove(table)
        group.arrange(RIGHT, buff=2)
        self.add(group)
