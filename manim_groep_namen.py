from manim import *


class Team_names(Scene):
    def construct(self):
        # We set up the names of the users
        group_name = Text("Groep 4:", font="DejaVu Sans").to_corner(UL)
        name1 = Text("Douwe Boonstoppel", font="DejaVu Sans", font_size =55)
        name2 = Text("Sude-Lara Bildirici", font="DejaVu Sans", font_size =55) 
        name3 = Text("Ciarán Connolly", font="DejaVu Sans", font_size =55)
        name4 = Text("Sara Porta Etssam", font="DejaVu Sans", font_size =55)

        names = VGroup(name1, name2, name3, name4).arrange(DOWN, center=False).to_edge(RIGHT)

        # we create the grid and show it
        grid = NumberPlane()
        self.add(grid)


        self.play(Create(grid, run_time=2))
        self.play(FadeIn(group_name, shift=DOWN))
        self.play(FadeIn(names, shift=UP))
        self.wait()

        grid.prepare_for_nonlinear_transform()
        self.play(
            ApplyPointwiseFunction(
                lambda p: p + np.array([np.sin(p[1]), np.sin(p[0]), 0]),
                VGroup(grid, names, group_name),
            ),
            run_time=3
        )
        self.wait()