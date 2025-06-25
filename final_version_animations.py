from manim import *
import numpy as np

#manim -pql hello.py Example
#.\venv\Scripts\activate    

#################################BELANGRIJK#################################

#Ciarán heeft Example en Flash geschreven
#Sude heeft Electron geschreven

class HelloWorld(Scene):
    def construct(self):
        self.wait(1)
        text = Text("Hello World")
        self.play(Write(text))
        self.wait(2)

class Example(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=85 * DEGREES, theta=5 * DEGREES)

        start_pos_muon_1 = 5*OUT+2*UP
        muon_1 = Dot3D().shift(start_pos_muon_1).set_opacity(0.4)
        self.play(Create(muon_1))

        start_pos_muon = 5*OUT+1*DOWN
        muon = Dot3D().shift(start_pos_muon).set_opacity(0.4)
        self.play(Create(muon))

        def make_trail_segment(start, end):
            return DashedLine(start=start, end=end, color=BLUE).set_opacity(0.4).set_glow_factor(0.5)

        trail_before = always_redraw(lambda: 
            make_trail_segment(
                start_pos_muon,
                muon.get_center() if muon.get_center()[2] > 1.2 else np.array([0, -0.62, 1.2])
            )
        )

        trail_after = always_redraw(lambda:
            make_trail_segment(
                np.array([0, -0.55, 0.5]) if (muon.get_center()[2] < 0.4) else np.array([0,-0.3,-2]),
                muon.get_center() if (-2 < muon.get_center()[2] < 0.5) else np.array([0,-0.3,-2])
            )
        )

        trail_after_after = always_redraw(lambda:
            make_trail_segment(
                np.array([0, -0.23, -2.7]) if muon.get_center()[2] < -2.7 else np.array([10,10,10]),
                muon.get_center() if muon.get_center()[2] < -2.7 else np.array([10,10,10])
            )
        )

        trail_1_before = always_redraw(lambda: 
            make_trail_segment(
                start_pos_muon_1,
                muon_1.get_center() if muon_1.get_center()[2] > 1.2 else np.array([0, 0.1, 1.2])
            )
        )

        trail_1_after = always_redraw(lambda:
            make_trail_segment(
                np.array([0, -0.25, 0.5]) if (muon_1.get_center()[2] < 0.4) else np.array([10,10,10]),
                muon_1.get_center() if (muon_1.get_center()[2] < 0.5) else np.array([10,10,10])
            )
        )

        #trail = always_redraw(lambda: DashedLine(start=(start_pos_muon), end=(muon.get_center()), color=BLUE))
        #trail.set_glow_factor(0.5).set_opacity(0.2)
        self.add(trail_1_before, trail_1_after)
        self.add(trail_before, trail_after, trail_after_after)

        table = Cube().scale([6,5,0.05]).set_color(DARK_GRAY).shift(OUT*0.78)
        self.add(table)

        blocks_dims = 0.6*np.array([6,1,0.5])
        block = Cube(fill_opacity=0.5).scale(blocks_dims).set_color(RED)
        block.shift(OUT)

        block2 = Cube(fill_opacity=0.5).scale(blocks_dims).set_color(RED)
        block2.shift(2*IN)

        #blocks = Group(block, block2).arrange(buff=1)
        self.play(Create(block))
        self.play(Create(block2))
        self.wait(1)

        self.play(muon_1.animate.shift(10*IN + 5*DOWN), run_time=1)
        self.play(FadeOut(trail_1_before, trail_1_after))

        self.wait(1)

        self.play(muon.animate.shift(10 * IN + UP), run_time=1)

        self.play(FadeOut(trail_before, trail_after, trail_after_after))

        line = DashedLine(start=(block.get_center() + np.array([blocks_dims[0], 0, -blocks_dims[2]])), end=(block2.get_center() + np.array([blocks_dims[0], 0, -blocks_dims[2]])))
        self.play(Create(line))
        self.wait(1)

        moving_line = always_redraw(lambda: DashedLine(start=(block.get_center() + np.array([blocks_dims[0], 0, -blocks_dims[2]])), end=(block2.get_center() + np.array([blocks_dims[0], 0, -blocks_dims[2]]))))
        self.add(moving_line)

        #angle = Angle(line, moving_line)
        #self.add(angle)

        self.play(block.animate.shift(2*UP), run_time = 3)
        self.wait(2)

        self.play(block.animate.shift(2*DOWN))

class Flash(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=85 * DEGREES, theta=5 * DEGREES)

        start_pos_muon = 10*OUT+1*DOWN
        muon = Dot3D().shift(start_pos_muon).set_opacity(0.4)
        self.play(Create(muon))

        table = Cube().scale([6,5,0.05]).set_color(DARK_GRAY).shift(OUT*0.78)
        self.add(table)

        blocks_dims = 0.6*np.array([6,1,0.5])
        block = Cube(fill_opacity=0.5).scale(blocks_dims).set_color(RED)
        block.shift(OUT)

        block2 = Cube(fill_opacity=0.5).scale(blocks_dims).set_color(RED)
        block2.shift(2*IN)

        #blocks = Group(block, block2).arrange(buff=1)
        self.add(block)
        self.add(block2)

        self.wait(2)

        self.move_camera(phi=0 * DEGREES, theta=45 * DEGREES, run_time = 3)
        
        self.remove(block2)

        self.wait(2)

        self.play(muon.animate.shift(9 * IN + UP), run_time=1)

        center = (OUT)
        num_particles = 20
        max_radius = 0.6

        particles = VGroup()
        animations = []

        for _ in range(num_particles):
            direction = np.random.normal(size=3)
            direction /= np.linalg.norm(direction)
            end_point = center + max_radius * direction

            particle = Sphere(radius=0.02).set_color(ORANGE)
            particle.move_to(center)
            particles.add(particle)

            animations.append(particle.animate.move_to(end_point))

        self.remove(muon)
        self.add(particles)
        self.play(*animations, run_time=1.2) 

        self.play(FadeOut(particles), run_time=1)
        self.wait(1)

class Electron(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=45 * DEGREES)

        table = Cube().scale([6, 5, 0.05]).set_color(DARK_GRAY).shift(OUT * 0.78)
        self.add(table)

        blocks_dims = 0.6 * np.array([6, 1, 0.5])
        block = Cube(fill_opacity=0.5).scale(blocks_dims).set_color(RED).shift(OUT)
        self.add(block)

        wire = Line3D(start=[-3.6,0,1], end=[-10,0,1]).set_color(RED)
        self.add(wire)

        self.wait(2)

        self.play(table.animate.shift([2,0,5]), block.animate.shift([2,0,5]), wire.animate.shift([2,0,5]), run_time=1)
        self.move_camera(phi=0 * DEGREES, theta=90 * DEGREES, run_time = 1)

        self.wait(2)

        foton = Sphere(radius=0.05).set_color(ORANGE)
        foton.move_to([6,0,7])
        self.add(foton)

        electron = Sphere(radius=0.05).set_color(YELLOW)
        electron.move_to([0,0,7])
        self.add(electron)


        metal = Cube().scale([0.2,0.5,0.2]).set_color(GRAY).set_opacity(1)
        metal.move_to([0,0,7])
        self.play(Create(metal))

        self.wait(4)

        metals = Cube().scale([0.05,0.2,0.2]).set_color(BLUE).set_opacity(1)
        metals.move_to([-0.6,0.3,7])
        self.play(Create(metals))

        metals2 = Cube().scale([0.05,0.2,0.2]).set_color(BLUE).set_opacity(1)
        metals2.move_to([-0.6,-0.3,7])
        self.play(Create(metals2))

        metals3 = Cube().scale([0.05,0.2,0.2]).set_color(BLUE).set_opacity(1)
        metals3.move_to([-1,0.3,7])
        self.play(Create(metals3))

        metals4 = Cube().scale([0.05,0.2,0.2]).set_color(BLUE).set_opacity(1)
        metals4.move_to([-1,-0.3,7])
        self.play(Create(metals4))

        self.wait(1)

        self.play(foton.animate.move_to([0,0,7]))

        self.play(electron.animate.move_to([-0.6,0.4,7]))

        elec2 = electron.copy()

        self.play(electron.animate.move_to([-1,0.26,7]), elec2.animate.move_to([-1,0.44,7]))

        elec3 = electron.copy()
        elec4 = elec2.copy()

        self.play(electron.animate.move_to([-1.5,0.11,7]), elec3.animate.move_to([-1.5,0.27,7]), elec2.animate.move_to([-1.5,0.48,7]), elec4.animate.move_to([-1.5,0.38,7]))

        self.remove(elec2, elec3, elec4)

        electron.move_to([-1.6,0,7])
        self.play(electron.animate.move_to([-7.6,0,7]))

        self.wait(2)