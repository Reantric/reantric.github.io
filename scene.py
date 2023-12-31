import random

import numpy as np
from manim import *

from util import pairwise
from math import sqrt

COL = "#2a2c40"
config.background_color = COL

textemp = r"""\usepackage{xcolor}
    \usepackage{bigints}
    \renewcommand{\c}[1]{\color{#1}}
    \def\mbb#1{\mathbb{#1}}
    \def\mfk#1{\mathfrak{#1}}

    \def\bN{\mbb{N}}
    \def\bC{\mbb{C}}
    \def\bR{\mbb{R}}
    \def\bQ{\mbb{Q}}
    \def\bZ{\mbb{Z}}
    \newcommand{\f}[2]{\frac{#1}{#2}}
    \newcommand{\sinf}[1]{\sum_{n =#1}^{\infty}}
    \newcommand{\linf}[1]{\lim_{x \to #1}^{\infty}}
    \newcommand{\deriv}[1]{\f{d}{d#1}}
    \newcommand{\vecD}[2]{\begin{bmatrix} 
        #1 \\
        #2
        \end{bmatrix}}

    \newcommand{\vecT}[3]{\begin{bmatrix} 
        #1 \\
        #2 \\ 
        #3
        \end{bmatrix}}
    \newcommand{\st}[1]{\sin(\theta)}    
    \newcommand{\ct}[1]{\cos(\theta)} 
    \newcommand{\x}[0]{\cdot} 
    \newcommand{\tu}[1]{\textup{#1}} 
    \colorlet{r}{red}
    \colorlet{o}{orange}
    \colorlet{c}{cyan}
    \colorlet{l}{lime}
    \colorlet{m}{magenta}
    \colorlet{b}{blue}
    \colorlet{y}{yellow}
    \colorlet{w}{white}
    \colorlet{p}{pink}

    \usepackage{tikz}
    \usetikzlibrary{fadings}
    \usepackage{pgffor}

    \pgfdeclarehorizontalshading{rainbow}{100bp}{%
      rgb(0bp)=(1,0,0);
      rgb(26bp)=(1,0,0);
      rgb(33bp)=(1,.5,0);
      rgb(40bp)=(1,1,0);
      rgb(47bp)=(0,1,0);
      rgb(54bp)=(0,1,0.5);
      rgb(61bp)=(0,1,1);
      rgb(68bp)=(1,0,1);
      rgb(75bp)=(.5,0,.5);
      rgb(100bp)=(.5,0,.5)}

    \newcommand\snow[2][]{%
      \begin{tikzfadingfrompicture}[name = fading letter]
        \node[text = transparent!0, inner xsep = 0pt, outer xsep = 0pt] {#2};
      \end{tikzfadingfrompicture}%
      \begin{tikzpicture}[baseline = (textnode.base)]
        \node[inner sep = 0pt, outer sep = 1pt] (textnode) {\phantom{#2}}; 
        \shade[path fading = fading letter, fading text, #1, fit fading = false]
        (textnode.south west) rectangle (textnode.north east);% 
      \end{tikzpicture}% 
    }

    \tikzset{fading text/.style = {shading=rainbow}}
    \usepackage{scalerel}
\usepackage{stackengine}
\newcommand{\longdiv}{\smash{\mkern-0.43mu\vstretch{1.31}{\hstretch{.7}{)}}\mkern-5.2mu\vstretch{1.31}{\hstretch{.7}{)}}}}"""

config.tex_template.add_to_preamble(textemp)


class RS(Scene):
    def construct(self):
        self.camera.background_color = COL  # set the background color to navy blue

        def func(t):
            return [t, np.exp(-t ** 2), 0]

        p = ParametricFunction(func, t_range=[-2, 2], fill_opacity=0)
        p.set_color_by_gradient([RED, BLUE, GREEN])
        numpl = NumberPlane(
            x_range=[-3, 3],
            y_range=[-2, 2],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            },
            axis_config={
                "include_numbers": True
            }
        )
        v = VGroup(numpl, p)
        v.scale(2)
        self.play(Create(numpl))

        self.play(Write(Dot(numpl.coords_to_point(0, 0))))
        self.play(Create(p))
        self.play(Write(numpl.get_riemann_rectangles(p, x_range=[-1, 1])))


class MyCamera(ThreeDCamera):
    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "fixed", False):
            return points
        else:
            return super().transform_points_pre_display(mobject, points)


class MyThreeDScene(ThreeDScene):
    def __init__(self, camera_class=MyCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)


def make_fixed(*mobs):
    for mob in mobs:
        mob.fixed = True
        for submob in mob.family_members_with_points():
            submob.fixed = True


def tex_init(lcs):
    lcs.stdtex = TexTemplate()
    # lcs.stdtex.add_to_preamble(textemp) PROBABLY UNNECCESSARY NOW?


class ThreeFunc(MyThreeDScene):
    def construct(self):
        tex_init(self)

        self.camera.background_color = COL

        def func(u, v):
            return np.array([
                u,
                v,
                np.exp(-(u ** 2 + v ** 2))
            ])

        s = Surface(
            func,
            u_range=[-2, 2],
            v_range=[-2, 2]
        )
        s.set_fill_by_checkerboard(GREEN, GREEN_A)

        axes = ThreeDAxes()

        surface = VGroup(axes, s)

        # Group together axes and surface
        def create_prisms(n):
            prisms = []
            du = 4 / n
            dv = 4 / n

            for i in range(n):
                for j in range(n):
                    x = -2 + i * du
                    y = -2 + j * dv
                    z = func(x, y)[2]
                    p = Prism(dimensions=[du, dv, z])
                    p.set_color(MAROON)
                    p.move_to([x, y, z / 2])
                    prisms.append(p)
            return VGroup(*prisms)

        tex = MathTex("{{f(x,y)}} = {{ e^{-(x^2 + y^2)} }}", tex_template=self.stdtex).to_edge(UP, buff=0.4)
        tex[2].set_color(YELLOW)
        texN = MathTex(
            "{{ \\int_{-2}^2 \\int_{-2}^2 }} {{ f(x,y) \\, }} {{ \\tu{d}x \\, \\tu{d}y }} {{ \\approx \\sum_{i=0}^{n-1} \\sum_{j=0}^{m-1} f(x_i,y_j) \\Delta A }}",
            tex_template=self.stdtex)
        texN[0].set_color("#bfff00")

        texN[6].set_color(LIGHT_PINK)
        texN.to_edge(UP * 2).to_edge(UP, buff=0.4)
        self.set_camera_orientation(0.8 * np.pi / 2, -0.45 * np.pi)

        # self.add_fixed_in_frame_mobjects(tex)
        box = SurroundingRectangle(tex, color=YELLOW, buff=SMALL_BUFF)
        box2 = SurroundingRectangle(texN, color=YELLOW, buff=SMALL_BUFF)
        make_fixed(tex, texN, box, box2)
        self.prisms = create_prisms(2)
        total = VGroup(surface, self.prisms)
        total.scale(2)
        self.add(surface)
        self.set_camera_orientation(frame_center=[0, 0, 1])
        self.add(box)
        self.begin_ambient_camera_rotation()

        # Start off with 2 rects
        self.n_var = MathTex("{{ n = m = }}", 2).to_edge(DOWN, buff=0.4).to_edge(RIGHT)
        self.n_var[1].set_color(ORANGE)
        make_fixed(self.n_var)
        addRects = AnimationGroup(ApplyMethod(surface.set_opacity, 0.2), AnimationGroup(
            LaggedStart(*[Write(p) for p in self.prisms], ReplacementTransform(box, box2), Write(self.n_var),
                        TransformMatchingTex(tex, texN))), lag_ratio=1, run_time=3)
        self.play(addRects)
        self.add_fixed_in_frame_mobjects(texN)
        self.wait()

        colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK]

        def reRiemann(n):
            total.remove(self.prisms)
            total.scale(0.5)
            prismsnw = create_prisms(n)
            total.add(prismsnw)
            total.scale(2)
            n_var1 = MathTex("{{ n = m = }}", n).to_edge(DOWN, buff=0.4).to_edge(RIGHT)
            random_color = random.choice(colors)
            n_var1[1].set_color(random_color)
            make_fixed(n_var1)
            self.play(FadeTransform(self.prisms, prismsnw), TransformMatchingTex(self.n_var, n_var1))
            self.n_var = n_var1

        # Update the prisms within the total VGroup
        reRiemann(4)
        self.wait()
        reRiemann(8)
        self.wait()
        reRiemann(20)
        # self.wait()
        reRiemann(30)
        self.wait(3)
    #  self.move_camera()


class VF(Scene):
    def construct(self):
        tex_init(self)
        self.camera.background_color = COL
        npl = NumberPlane()

        t = ValueTracker(0)

        def func(pos, dt):
            return np.sin(pos[1] + dt) * RIGHT + np.cos(pos[0] + dt) * UP

        vector_field = always_redraw(
            lambda: ArrowVectorField(lambda pos: func(pos, t.get_value())).scale(2)
        )

        mtx = MathTex(r"f: {{ \mathbb{R}^2 \to \mathbb{R}^2 }}").to_edge(UP, buff=0.4)
        mtx[1].set_color(ORANGE)
        box = SurroundingRectangle(mtx, color=WHITE, buff=SMALL_BUFF).set_fill(color=BLACK, opacity=1)
        self.play(Create(npl), Write(vector_field), Create(box), Write(mtx))
        self.play(t.animate.set_value(2 * PI), run_time=5, rate_func=rate_functions.ease_in_out_cubic)
        self.wait()


class PictureScene(Scene):
    def construct(self):
        def sub(self, other):
            return Line(self.get_start() - other.get_start(), self.get_end() - other.get_end())

        Line.__sub__ = sub

        # Number plane
        npl = NumberPlane()

        # Vectors
        vector_1 = Vector([2, 1]).set_color(YELLOW)
        vector_2 = Vector([3, -1]).set_color("#AFEEEE")

        # Angle indicator
        angle = Angle(vector_2, vector_1, radius=0.5, color=RED)
        theta_label = MathTex("\\theta").next_to(angle, RIGHT, buff=0.12).set_color("#da70d6")

        vector_1_np = np.array([2, 1, 0])
        vector_2_np = np.array([3, -1, 0])
        dot_product = np.dot(vector_1_np, vector_2_np)
        magnitude_squared = np.dot(vector_2_np, vector_2_np)
        projection = (dot_product / magnitude_squared) * vector_2_np
        projection_vector = Vector(projection).set_color(ORANGE)

        dashed_line = DashedLine(vector_1.get_end(), projection_vector.get_end(), dash_length=0.1).set_color(GRAY)

        a_label = MathTex(r"\vec{a}").next_to(vector_1.get_end(), UP, buff=0.15).set_color(YELLOW)
        b_label = MathTex(r"\vec{b}").next_to(vector_2.get_end(), RIGHT, buff=0.15).set_color("#AFEEEE")
        proj_label_text = "\\text{proj}_{\\vec{b}} \\vec{a}"
        angle_of_projection = np.arctan2(projection[1], projection[0])
        proj_label = MathTex(proj_label_text).next_to(projection_vector, DOWN, buff=-0.1).rotate(
            angle_of_projection).set_color(ORANGE)

        right_angle = RightAngle(line1=projection_vector, line2=Line(vector_1.get_end(), projection_vector.get_end()),
                                 length=0.25, color=BLUE, quadrant=(-1, -1))

        v = VGroup(npl, right_angle, vector_1, vector_2, projection_vector, dashed_line, angle, theta_label, a_label,
                   b_label,
                   proj_label)
        v.scale(2.0)

        # Add to scene
        self.add(v)


class CrossProductScene(ThreeDScene):
    def construct(self):
        # Set the camera position
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # Create the 3D axes
        axes = ThreeDAxes()

        # Create the first vector (lime color)
        vec1 = Arrow3D(start=[0, 0, 0], end=[0.75, 1.5, 0], color="#32CD32")
        vec1_label = MathTex("\\vec{a}").set_color("#32CD32")
        vec1_label.next_to(vec1.get_end(), direction=DOWN + RIGHT, buff=0.3)

        # Create the second vector (pink color)
        vec2 = Arrow3D(start=[0, 0, 0], end=[1, 1, 2], color=PINK)
        vec2_label = MathTex("\\vec{b}").set_color(PINK)
        vec2_label.next_to(vec2.get_end(), direction=UP + LEFT, buff=0.6)

        # Calculate the cross product of the two vectors
        cross_product = np.cross([0.75, 1.5, 0], [1, 1, 2])
        vec3 = Arrow3D(start=[0, 0, 0], end=cross_product, color=ORANGE)
        vec3_label = MathTex("\\vec{a} \\times \\vec{b}").set_color(ORANGE)
        vec3_label.next_to(vec3.get_end(), direction=RIGHT)

        # Create a plane spanned by vec1 and vec2
        plane = Polygon([0, 0, 0], vec1.get_end(), vec1.get_end() + vec2.get_end(), vec2.get_end(), color=BLUE)
        plane.set_opacity(0.4)  # Set the transparency

        # Add the plane first so it's in the background
        self.add(axes, plane, vec1, vec2, vec3)

        # Add text labels with fixed orientation in 3D space
        self.add_fixed_orientation_mobjects(vec1_label, vec2_label, vec3_label)


class VFScene(Scene):
    def construct(self):
        tex_init(self)
        # Define the scale factor
        scale_factor = 2

        # Define the vector function
        def vector_func(t):
            return np.array([scale_factor * np.cos(t), scale_factor * np.sin(t), 0])

        # Define the value tracker for time
        t_tracker = ValueTracker(0)

        # Define the vector and its position update function
        vector = Vector(vector_func(t_tracker.get_value())).set_color(GREEN_A)
        vector.add_updater(
            lambda m: m.become(Vector(vector_func(t_tracker.get_value())).set_color(GREEN_B).shift((DOWN + LEFT))))
        txt = MathTex("t")

        # Define the slider
        slider = NumberLine(x_range=[0, 2 * np.pi, np.pi], include_numbers=False)
        slider.add_labels({0: 0, np.pi: MathTex(r"\pi"), 2 * np.pi: MathTex(r"2\pi")})
        dot = Dot()
        dot.add_updater(
            lambda m: m.move_to(slider.point_from_proportion(t_tracker.get_value() / (2 * np.pi))).set_color(GREEN_A))
        ptr = Arrow().rotate(PI / 2).set_color(RED)
        ptr.add_updater(lambda m: m.next_to(dot, direction=DOWN))
        txt.add_updater(lambda m: m.next_to(ptr.get_start(), direction=DOWN).set_color(ORANGE))

        # Group slider, dot and pointer
        slider_group = VGroup(slider, dot, ptr, txt).to_corner(UP + RIGHT, buff=0.3)

        # Create the number plane
        npl = NumberPlane().scale(2)

        # Define the labels
        labels = [
            Tex("1").next_to(npl.c2p(1, 0), DOWN),
            Tex("-1").next_to(npl.c2p(-1, 0), DOWN),
            Tex("1").next_to(npl.c2p(0, 1), LEFT, buff=0.17),
            Tex("-1").next_to(npl.c2p(0, -1), LEFT, buff=0.17)
        ]

        def color_map(value):
            # Convert the input value to a value between 0 and 1
            normalized_value = value / (2 * np.pi)

            # Get the color from the hsv colormap, which is a rainbow colormap
            color = plt.cm.hsv(normalized_value)

            # Convert color to HEX form
            hex_color = mcolors.rgb2hex(color[:3])

            return hex_color

        totparts = 800
        lines = VGroup(*[Line(
            vector_func((x - 1) * 2 * np.pi / totparts),
            vector_func(x * 2 * np.pi / totparts)
        ).set_color(color_map(x * 2 * np.pi / totparts)) for x in range(1, totparts + 1)])
        lines.set_opacity(0)

        def update_lines(m):
            # Calculate the corresponding points on the curve
            k = integer_interpolate(0, totparts, t_tracker.get_value() / (2 * np.pi))
            v = k[0]
            if k[1] > 0.8:
                v += 1
            m[:v].set_opacity(1)

        lines.add_updater(update_lines)

        #   bg = [BackgroundRectangle(x,fill_color=BLACK,fill_opacity=0.2,buff=0.1) for x in labels]

        # Add objects to the scene
        tg = VGroup(npl, vector, lines, *labels)
        tg.shift((DOWN + LEFT))
        mt = MathTex(r"\vec{r}(t) = \vecD{\cos(t)}{\sin(t)}", tex_template=self.stdtex).set_color(PINK).to_corner(
            UP + LEFT,
            buff=0.8).shift(
            RIGHT * 0.35).scale(1.5)
        mt.add_background_rectangle(BLACK, opacity=0.5, buff=0.25)

        self.add(tg, slider_group, mt)
        # Animate
        self.play(t_tracker.animate.set_value(2 * np.pi), run_time=8, rate_func=rate_functions.ease_in_out_cubic)


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from manim import *


class ShoelaceFormula(Scene):
    def construct(self):
        # Initialize the points for the vertices of the polygon
        points = [
            np.array([2 * np.cos(2 * np.pi * n / 5 + np.random.uniform(-1.0, 1.0)),
                      2 * np.sin(2 * np.pi * n / 5 + np.random.uniform(-1.0, 1.0)), 0])
            for n in range(5)
        ]

        # Create the polygon
        polygon = Polygon(*points, stroke_width=2)

        # Create a group to store the triangles
        triangles = VGroup()
        col = [RED, GREEN, YELLOW, PURPLE_A, BLUE]

        # Loop over each vertex and create a triangle with the next vertex and the center
        for n in range(5):
            random_color = col[n]
            triangle = Polygon(ORIGIN, points[n], points[(n + 1) % 5], stroke_width=3.5, stroke_color=random_color,
                               fill_color=random_color, fill_opacity=0.6)
            triangles.add(triangle)

        # Add a NumberPlane to the scene
        self.add(NumberPlane())

        vectors = VGroup()

        for i in range(5):
            vec = Vector(points[i], color=col[i])
            label = MathTex(f"v_{i + 1}").next_to(vec, direction=vec.get_unit_vector(), buff=0.2).set_color(col[i])
            vectors.add(vec, label)

        # Add the polygon, the triangles, and the vectors to the scene
        v = VGroup(vectors, polygon, triangles)
        v.scale(1.5)
        self.add(v)

        self.wait(2)


class ParameterisedCurve1(Scene):
    def construct(self):
        tex_init(self)
        # Define the scale factor
        scale_factor = 2

        # Define the vector function
        def vector_func(t):
            return np.array([scale_factor * np.cos(t), scale_factor * np.sin(t), 0])

        def vector_func2(t):
            return np.array([scale_factor * np.cos(2 * t), scale_factor * np.sin(2 * t), 0])

            # Define the value tracker for time

        t_tracker = ValueTracker(0)
        SHIFT = 3 * RIGHT
        # Define the vector and its position update function
        vector = Vector(vector_func(t_tracker.get_value())).set_color(RED)
        vector.add_updater(
            lambda m: m.become(Vector(vector_func(t_tracker.get_value())).set_color(RED).shift(SHIFT)))
        txt = MathTex("t")

        vector2 = Vector(vector_func2(t_tracker.get_value())).set_color(GREEN)
        vector2.add_updater(
            lambda m: m.become(Vector(vector_func2(t_tracker.get_value())).set_color(GREEN).shift(SHIFT)))

        # Define the slider
        slider = NumberLine(x_range=[0, 2 * np.pi, np.pi], include_numbers=False)
        slider.add_labels({0: 0, np.pi: MathTex(r"\pi"), 2 * np.pi: MathTex(r"2\pi")})
        dot = Dot()
        dot.add_updater(
            lambda m: m.move_to(slider.point_from_proportion(t_tracker.get_value() / (2 * np.pi))).set_color(GREEN_A))
        ptr = Arrow().rotate(-PI / 2).set_color(BLUE)
        ptr.add_updater(lambda m: m.next_to(dot, direction=UP))
        txt.add_updater(lambda m: m.next_to(ptr.get_start(), direction=UP).set_color(BLUE))

        # Group slider, dot and pointer
        slider_group = VGroup(slider, dot, ptr, txt).to_corner(DOWN + 2 * LEFT, buff=0.3)

        # Create the number plane
        npl = NumberPlane().scale(2)

        # Define the labels
        labels = [
            Tex("1").next_to(npl.c2p(1, 0), DOWN),
            Tex("-1").next_to(npl.c2p(-1, 0), DOWN),
            Tex("1").next_to(npl.c2p(0, 1), LEFT, buff=0.17),
            Tex("-1").next_to(npl.c2p(0, -1), LEFT, buff=0.17)
        ]

        curve = always_redraw(lambda:
                              ParametricFunction(vector_func, t_range=[0, t_tracker.get_value()], color=RED).shift(
                                  (SHIFT))
                              )

        curve2 = always_redraw(lambda:
                               ParametricFunction(vector_func2, t_range=[0, t_tracker.get_value()], color=GREEN).shift(
                                   (SHIFT))
                               )
        tg = VGroup(npl, vector2, vector, *labels)
        tg.shift((SHIFT))
        mt = MathTex(r"\vec{r_1}(t) = \vecD{\cos(t)}{\sin(t)}", tex_template=self.stdtex).set_color(RED).to_corner(
            UP + LEFT,
            buff=0.8).shift(
            RIGHT * 0.35 + UP * 0.175 + LEFT * 0.29).scale(1)
        mt.add_background_rectangle(BLACK, opacity=0.5, buff=0.25)

        mt2 = MathTex(r"\vec{r_2}(t) = \vecD{\cos(2t)}{\sin(2t)}", tex_template=self.stdtex).set_color(GREEN).next_to(
            mt, direction=DOWN, buff=0.5)
        mt2.add_background_rectangle(BLACK, opacity=0.5, buff=0.25)

        self.add(tg, slider_group,
                 curve2, curve, mt, mt2
                 )

        self.play(
            t_tracker.animate.set_value(2 * np.pi),
            run_time=10,
            # rate_func=rate_functions.ease_in_out_cubic
        )


class LongD(Scene):
    def construct(self):
        tex_init(self)
        # Create the dividend and divisor
        tst = MathTex(r"""
\arraycolsep=1pt
\renewcommand\arraystretch{1.2}
\begin{array}{*1r @{\hskip\arraycolsep}c@{\hskip\arraycolsep} *{11}r}
        &          & 1 & 1 & 1 & 1 \dots  \\
\cline{2-13}
1-x-x^2 & \longdiv & 1 &   &   &   &      &   &      &   &      &   &        \\
        &          & 1 & - & x & - &  x^2 &   &      &   &      &   &        \\
\cline{3-7}
        &          &   &   & x & + &  x^2 &   &      &   &      &   &        \\
        &          &   &   & x & - &  x^2 & - &  x^3 &   &      &   &        \\
\cline{5-9}
        &          &   &   &   &   & 2x^2 & - &  x^3 &   &      &   &        \\
        &          &   &   &   &   & 2x^2 & - & 2x^3 & - & 2x^4 &   &        \\
\cline{7-11}
        &          &   &   &   &   &      &   & 3x^3 & + & 2x^4 &   &        \\
        &          &   &   &   &   &      &   & 3x^3 & - & 3x^4 & - & 3x^5   \\
\cline{9-13}
        &          &   &   &   &   &      &   &      &   & 5x^4 & + & 3x^5   \\
        &          &   &   &   &   &      &   &      &   &      &   & \vdots \\
\end{array}

""", tex_template=self.stdtex)
        self.add(tst)


class Slider:
    lower = 0
    upper = 2 * np.pi
    dot_color = GREEN_A
    texT_color = BLUE
    vector_color = BLUE
    ptr = None
    txt = None

    def add_labels(self, slider, labels):
        slider.add_labels(labels)

        # retrofit later
        ticks = VGroup(
            *[Line(start=slider.n2p(x) - 0.2 * UP, end=slider.n2p(x) + 0.2 * UP, stroke_width=2) for x in [-4, 2]]
        )

    def change_vector_color(self,c):
        self.vector_color = c
        self.ptr.set_color(c)
        return self

    def change_text_col(self,c):
        self.texT_color = c
        self.txt.set_color(c)
        return self


    def __init__(self, range=[0, 2 * np.pi, np.pi], length=5,
                 labels={0: 0, np.pi: MathTex(r"\pi"), 2 * np.pi: MathTex(r"2\pi")}):
        self.txt = MathTex("t")
        self.lower = range[0]
        self.upper = range[1]
        self.t_tracker = ValueTracker(self.lower)

        slider = NumberLine(
            x_range=range,
            length=5,
            include_numbers=False,  # we're going to manually add the numbers
            decimal_number_config={
                "num_decimal_places": 0,
                "include_sign": False,
            },
            label_direction=DOWN,  # Ensures that labels are not placed over ticks
        )
        self.add_labels(slider, labels)

        dot = Dot()
        dot.move_to(
            slider.point_from_proportion(self.t_tracker.get_value() / (self.upper - self.lower))).set_color(
            self.dot_color)
        dot.add_updater(
            lambda m: m.move_to(
                slider.point_from_proportion(self.t_tracker.get_value() / (self.upper - self.lower))).set_color(
                self.dot_color))
        self.ptr = Arrow().rotate(-PI / 2).set_color(self.vector_color)
        self.ptr.next_to(dot, direction=UP)
        self.ptr.add_updater(lambda m: m.next_to(dot, direction=UP).set_color(self.vector_color))
        self.txt.next_to(self.ptr.get_start(), direction=UP).set_color(self.texT_color)
        self.txt.add_updater(lambda m: m.next_to(self.ptr.get_start(), direction=UP).set_color(self.texT_color))

        # Group slider, dot and pointer
        self.slider_group = VGroup(slider, dot, self.ptr, self.txt).to_corner(DOWN + 2 * LEFT, buff=0.3)


class TangentVectorParametric(Scene):

    def construct(self):
        slider = Slider(range=[0, np.pi, np.pi / 2], labels={})
        # {0:0,np.pi/2:MathTex(r"\f{\pi}{2}"),np.pi:MathTex(r"\pi")}
        slider_group = slider.slider_group
        SHIFT = 3.7 * LEFT + 1.25 * DOWN
        slider_group.scale(1.2).shift(RIGHT * 0.35 + UP * 0.15)
        self.add(slider_group)
        scale_factor = 2

        def vector_func(t):
            return np.array([scale_factor * 1.5 * t, scale_factor * (np.cos(t) + t), 0])

        parafunc = ParametricFunction(vector_func, t_range=[0, np.pi]).shift(SHIFT).set_color(RED)
        self.add(parafunc)

        def color_map(value):
            # Convert the input value to a value between 0 and 1
            normalized_value = value / (2 * np.pi)

            # Get the color from the hsv colormap, which is a rainbow colormap
            color = plt.cm.hsv(normalized_value)

            # Convert color to HEX form
            hex_color = mcolors.rgb2hex(color[:3])

            return hex_color

        vector = Vector([1.5, 1 - np.sin(0), 0]).set_color(WHITE)

        rprime = MathTex(r"\vec{r'}(t)").next_to(vector, direction=DOWN, buff=0.15)
        rprime.add_updater(lambda v: v.next_to(vector, direction=DOWN, buff=0.15).set_color(vector.get_color()))
        self.add(vector, rprime)
        self.play(vector.animate.move_to(vector_func(0) + SHIFT).set_color(color_map(0.34)))

        def vectorUpdater(v):
            dummy = Vector([1.5, 1 - np.sin(slider.t_tracker.get_value()), 0])
            dummy.shift(vector_func(slider.t_tracker.get_value()) - (dummy.get_start() + dummy.get_end()) / 2)
            dummy.shift(SHIFT).set_color(color_map(slider.t_tracker.get_value() + 0.34))
            v.become(dummy)

        vector.add_updater(vectorUpdater)

        self.play(
            slider.t_tracker.animate.set_value(slider.upper), run_time=5)


class NormalVector1(MovingCameraScene):
    scale_factor = 2
    SHIFT = 3.7 * LEFT + 2.8 * DOWN

    def drawVector(self, v: Vector):
        v.shift(((v.get_start() + v.get_end()) / 2 - v.get_start()))
        return v

    def vector_func(self, t):
        return np.array([self.scale_factor * 1.5 * t, self.scale_factor * (3 - 2 * np.arctan(t) - np.cos(t)), 0])

    def vector_funcd(self, t):
        return np.array([self.scale_factor * 1.5, self.scale_factor * (-2 / (t * t + 1) + np.sin(t)), 0])

    def fixed_zoomed_mob(self, mob, refFrame, DIRE=DOWN, currSCF=1):
        frame = self.camera.frame

        mob_center = mob.get_center()
        mob_uv = normalize(mob_center)
        mob_mod = np.linalg.norm(mob_center)
        mob_prop = mob_mod / (START_FRAME_WIDTH * currSCF)
        mob_width = mob.width / (START_FRAME_WIDTH * currSCF)

        def updater(_mob, referenceFrame, DIRE):
            fw = frame.width
            new_mod = mob_prop * fw
            new_width = mob_width * fw
            _mob.width = new_width
            #  print(frame.width,START_FRAME_WIDTH,0.15 * (frame.width/START_FRAME_WIDTH)**2)
            mob.next_to(referenceFrame, direction=DIRE, buff=0.15 * (frame.width / (START_FRAME_WIDTH * currSCF)))

        #   _mob.move_to(
        #      frame.get_center() + mob_uv * new_mod
        #  )

        mob.add_updater(lambda t: updater(t, refFrame, DIRE))

    def construct(self):
        parafunc = ParametricFunction(lambda t: self.vector_func(t), t_range=[0, np.pi]).shift(self.SHIFT).set_color(
            RED)
        self.add(parafunc)

        c = 0.35

        # Create a ValueTracker and get the path function of the curve

        # Move the camera to the start of the path

        def color_map(value):
            # Convert the input value to a value between 0 and 1
            normalized_value = value / (2 * np.pi)

            # Get the color from the hsv colormap, which is a rainbow colormap
            color = plt.cm.hsv(normalized_value)

            # Convert color to HEX form
            hex_color = mcolors.rgb2hex(color[:3])

            return hex_color

        vector = Vector(self.vector_funcd(c))
        dummy = Vector(vector.get_unit_vector())
        dummy.shift(self.vector_func(c) - (dummy.get_start() + dummy.get_end()) / 2)
        dummy.shift(self.SHIFT).set_color(color_map(1))
        vector.become(dummy)

        rprime = MathTex(r"\vec{T}(t)").next_to(vector, direction=DOWN + LEFT, buff=0.15).set_color(vector.get_color())
        self.fixed_zoomed_mob(rprime, vector.get_end(), DOWN + LEFT)
        tanV = VGroup(vector, rprime)
        self.add_foreground_mobject(tanV)

        self.play(self.camera.frame.animate.scale(0.4).move_to(self.vector_func(c) + self.SHIFT))

        h = ValueTracker(0.5)
        vector2 = Vector(self.vector_funcd(c + h.get_value()))

        dummy = Vector(vector2.get_unit_vector())
        dummy.shift(self.vector_func(c + h.get_value()) - (dummy.get_start() + dummy.get_end()) / 2)
        dummy.shift(self.SHIFT).set_color(color_map(1 + 3 * h.get_value()))
        vector2.become(dummy).set_opacity(0.3)

        def vectorUpdater(v):
            dv = self.vector_funcd(c + h.get_value())
            dummy = Vector(dv / np.linalg.norm(dv))
            dummy.shift(self.vector_func(c + h.get_value()) - (dummy.get_start() + dummy.get_end()) / 2)
            dummy.shift(self.SHIFT).set_color(color_map(1 + 3 * h.get_value()))
            v.become(dummy).set_opacity(0.3)

        vector2.add_updater(vectorUpdater)
        rprime2 = MathTex(r"\vec{T}(t+{{h}})").scale(0.4).next_to(vector2.get_end(), direction=UP + RIGHT,
                                                                  buff=0.05).set_color(
            vector2.get_color())
        rprime2[1].set_color(color_map(1 + 3 * h.get_value()))  # maybe set h to diff color

        v3 = vector2.copy()
        v3.remove_updater(vectorUpdater)

        vg2 = VGroup(vector2, rprime2)

        self.play(Write(vg2))

        self.fixed_zoomed_mob(rprime2, v3.get_end(), DIRE=UP + LEFT, currSCF=0.4)

        self.wait()

        def rprime2Upd2(v: MathTex):
            v.set_color(color_map(1 + 3 * h.get_value()))
            v.next_to(v3.get_end(), buff=0.05, direction=UP + RIGHT)
            return v

        rprime2.add_updater(rprime2Upd2)

        def v3Update(v: Vector):
            v.become(vector2.copy().remove_updater(vectorUpdater).set_color(vector2.get_color()).move_to(
                vector.get_start() + (-vector2.get_start() + vector2.get_end()) / 2)).set_opacity(1)
            return v

        self.play(v3.animate.move_to(vector.get_start() + (-v3.get_start() + v3.get_end()) / 2).set_opacity(1))
        v3.add_updater(v3Update)

        self.wait()

        self.play(self.camera.frame.animate.scale(0.3).move_to(vector.get_end()),
                  h.animate.set_value(0.3), run_time=5)

        rejection = Vector(self.vector_funcd(c + h.get_value()) / np.linalg.norm(
            self.vector_funcd(c + h.get_value())) - self.vector_funcd(c) / np.linalg.norm(
            self.vector_funcd(c))).move_to(vector.get_end())
        # print(h.get_value(),rejection.get_end() - rejection.get_start())
        rejection = self.drawVector(rejection)
        rejection.set_color(BLUE)

        r3 = MathTex(r"h \x \vec{N}(t)").set_color(BLUE).scale(0.4 * 0.6).next_to(rejection, buff=0.06,
                                                                                  direction=RIGHT).shift(UP * 0.03)
        self.play(DrawBorderThenFill(rejection), DrawBorderThenFill(r3))

        right_angle = RightAngle(line1=vector, line2=rejection,
                                 length=0.055, color=PINK, quadrant=(-1, 1)).set_stroke(width=1)
        self.add_foreground_mobject(right_angle)
        self.play(Create(right_angle))
        self.wait()

        # addupdtrs
        r3.add_updater(lambda t: t.next_to(rejection, buff=0.06, direction=RIGHT).shift(UP * 0.03))
        right_angle.add_updater(lambda t: t.become(RightAngle(line1=vector, line2=rejection,
                                                              length=0.055, color=PINK, quadrant=(-1, 1)).set_stroke(
            width=1)))
        self.play(self.camera.frame.animate.move_to(self.vector_func(c) + self.SHIFT), rejection.animate.move_to(
            self.vector_func(c) + self.SHIFT + (rejection.get_end() - rejection.get_start()) / 2))
        self.wait()

        newRejec = self.drawVector(Vector(1 / h.get_value() * (self.vector_funcd(c + h.get_value()) / np.linalg.norm(
            self.vector_funcd(c + h.get_value())) - self.vector_funcd(c) / np.linalg.norm(
            self.vector_funcd(c)))).move_to(self.vector_func(c) + self.SHIFT)).set_color(BLUE)
        r3.remove_updater(lambda t: t.next_to(rejection, buff=0.06, direction=RIGHT))
        newR3 = MathTex(r"\vec{N}(t)").set_color(BLUE).scale(0.4 * 1.2).next_to(newRejec, buff=0.1, direction=RIGHT)

        newRangle = RightAngle(line1=vector, line2=newRejec,
                               length=0.13, color=PINK, quadrant=(-1, 1)).set_stroke(width=1.7)

        newRejec.add_updater(lambda t: t.become(self.drawVector(Vector(1 / h.get_value() * (
                    self.vector_funcd(c + h.get_value()) / np.linalg.norm(
                self.vector_funcd(c + h.get_value())) - self.vector_funcd(c) / np.linalg.norm(
                self.vector_funcd(c)))).move_to(self.vector_func(c) + self.SHIFT)).set_color(BLUE)))
        newRangle.add_updater(lambda t: t.become(RightAngle(line1=vector, line2=newRejec,
                                                            length=0.13, color=PINK, quadrant=(-1, 1)).set_stroke(
            width=1.7)))
        self.play(self.camera.frame.animate.scale(2.5), rejection.animate.scale(1 / h.get_value()),
                  Transform(rejection, newRejec), Transform(right_angle, newRangle), TransformMatchingTex(r3, newR3),
                  run_time=2.5)
        self.remove(right_angle, rejection)
        self.add(newRejec, newRangle)
        self.wait()
        self.play(Write(MathTex(r"h \to 0").set_color(ORANGE).scale(0.5).shift(0.85 * DOWN + 3.2 * LEFT)))
        self.play(h.animate.set_value(0.0001), run_time=5)


from manim import *

START_FRAME_WIDTH = config.frame_width
START_FRAME_HEIGHT = config.frame_height
ASPECT_RATIO = START_FRAME_WIDTH / START_FRAME_HEIGHT


class Testor(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame
        txt_1 = MathTex("x^2").move_to(UP * 3 + RIGHT * 2)
        txt_2 = Vector([1, 1, 0]).move_to(DOWN * 3 + LEFT * 4)
        self.add(NumberPlane())
        self.add(txt_1)

        self.fixed_zoomed_mob(txt_1)

        self.add(txt_1, txt_2)
        self.play(
            frame.animate.scale(0.4),
            run_time=4
        )
        self.wait()

    def fixed_zoomed_mob(self, mob):
        frame = self.camera.frame

        mob_center = mob.get_center()
        mob_uv = normalize(mob_center)
        mob_mod = np.linalg.norm(mob_center)
        mob_prop = mob_mod / START_FRAME_WIDTH
        mob_width = mob.width / START_FRAME_WIDTH

        def updater(_mob):
            fw = frame.width
            new_mod = mob_prop * fw
            new_width = mob_width * fw
            _mob.width = new_width
            _mob.move_to(
                frame.get_center() + mob_uv * new_mod
            )

        mob.add_updater(updater)

import re
class ArcLengthFormula(Scene):
    scale_factor = 2
    SHIFT = 4.7 * LEFT + 0.65 * DOWN

    eqs = [
    ]

    #  (MathTex(r"\sum_{i=1}^n", r"\sqrt{", r"\left(r_x(t_i + \Delta t) - r_x(t_i)\right)^2", "+",
    #                       r"\left(r_y(t_i + \Delta t) - r_y(t_i)\right)^2", "}"),[
    #             [0, 1, 2, 3, 4, 5],
    #             #  | |      | |  |   |  |
    #             [0, 1, 2, 3, 4, 5],
    #
    #         ]),
    eq0 = None
    ntx = 0
    def texTransform(self,ind):
        #MathTex(r"\sum_{i=1}^n", r"\sqrt{", r"\left(r_x(t_{i+1}) - r_x(t_i)\right)^2", "+",
                  #    r"\left(r_y(t_{i+1}) - r_y(t_i)\right)^2}", "}")
        ti = self.eqs[ind][1]
        eq1 = self.eqs[ind][0]
      #  eq1.align_to(self.eq0, UR)

        def getTexTransform(transform_indices):
                return [
                    Create(eq1[j]) if i is None else
                    ReplacementTransform(self.eq0[i], eq1[j]) if (type(i) is not str and j is not None) else
                    FadeOut(self.eq0[int(re.search(r'\d+', str(i)).group())]) if (str(i)[-1] == "f" or j is None) else
                    ReplacementTransform(self.eq0[int(i[:-1])].copy(), eq1[j], path_arc=90 * DEGREES)
                    for i, j in zip(*transform_indices)
                ]

        v = getTexTransform(ti)
        self.eq0 = eq1
        return v



    def vector_func(self, t):
        return np.array(
            [self.scale_factor * 1.5 * t, self.scale_factor * (2 - 2 * np.arctan(t) - np.cos(t * t - 0.5)), 0])

    def vector_funcd(self, t):
        return NotImplementedError  # np.array([self.scale_factor * 1.5, self.scale_factor * (-2/(t*t + 1) + np.sin(t)), 0])

    def construct(self):
        parafunc = ParametricFunction(lambda t: self.vector_func(t), t_range=[0, np.pi]).shift(self.SHIFT).set_color(
            RED)
        self.add(parafunc)
        self.eq0 = MathTex(r"\sum_{i=1}^n", r"\left|", r"\vec{r}(t_{i+1})", "-", r"\vec{r}(t_{i})", r"\right|").scale(
            1.3).set_color(GREEN).next_to(parafunc, direction=UP)
        self.add(self.eq0)

        def color_map(value):
            # Convert the input value to a value between 0 and 1
            normalized_value = value / (np.pi)

            # Get the color from the hsv colormap, which is a rainbow colormap
            color = plt.cm.hsv(normalized_value)

            # Convert color to HEX form
            hex_color = mcolors.rgb2hex(color[:3])

            return hex_color

        def create_lines(n):
            lines = VGroup()
            for t1, t2 in pairwise(np.linspace(0, np.pi, n, endpoint=True)):
                lines.add(Line(self.vector_func(t1), self.vector_func(t2)).shift(self.SHIFT).set_color(
                    color_map(t1))).set_stroke(width=5)

            return lines

        lns = create_lines(3)
        self.n_var = MathTex("n","=", 2).to_edge(DOWN, buff=0.4).to_edge(RIGHT)
        self.n_var[1].set_color(ORANGE)
        self.play(Write(lns), Write(self.n_var))
        self.wait(2)

        self.eqs.append((MathTex(
            r"\sum_{i=1}^n", r"\sqrt{", r"\left(r_x(t_{i+1})", "-", r"r_x(t_i)\right)^2", "+", r"\left(r_y(t_{i+1})" ,"-", r"r_y(t_i)\right)^2","}").set_color(
            GREEN).next_to(parafunc, direction=UP),
            [[0,1,2,"2c","2c",3, 4, "4c","4c",5],
            #  | |      | |  |   |  |
            [0,1,2, 3,   4,  5, 6, 7,    8,  9],

        ]))
        self.eqs[self.ntx][0][1:9].set_color(ORANGE)


        self.play(
            LaggedStart(*self.texTransform(0), run_time=3.5))

        self.wait(0.5)

        def transform_lines(n, do = False, run_time=3.5):
            lns2 = create_lines(n)
            if n < 100:
                n_var1 = MathTex("n", "=", n - 1).to_edge(DOWN, buff=0.4).to_edge(RIGHT)
            else:
                n_var1 = MathTex(r"n" ,r"\to", r"\infty").to_edge(DOWN, buff=0.4).to_edge(RIGHT)
            random_color = color.random_bright_color()
            n_var1[1].set_color(random_color)

            self.wait()
            if do:
                self.play(
                AnimationGroup(Transform(lns, lns2), *[ReplacementTransform(self.n_var[x], n_var1[x]) for x in range(3)], *self.texTransform(self.ntx), run_time=run_time))
            else:
                self.play(AnimationGroup(Transform(lns, lns2), *[ReplacementTransform(self.n_var[x], n_var1[x]) for x in range(3)], run_time=run_time))

            self.remove(lns)
            self.add(lns2)
            self.n_var = n_var1
            return lns2

        temp = MathTex(
            # 0                1                   2                   3           4              5          6                      7        8                  9
            r"\sum_{i=1}^n", r"\sqrt{", r"\left(r_x(t_i + \Delta t)", "-", r"r_x(t_i)\right)^2", "+", r"\left(r_y(t_i + \Delta t)", "-", r"r_y(t_i)\right)^2", "}").set_color(
            GREEN).next_to(parafunc, direction=UP)
        temp[1:9].set_color(ORANGE)
        self.eqs.append((temp,[[x for x in range(10)],[x for x in range(10)]]))
        self.ntx += 1
        lns = transform_lines(7,True)

        temp = MathTex(
            #     0              1         2                    3                  4          5    6      7               8                          9       10  11
            r"\sum_{i=1}^n", r"\sqrt{",r"\left(", r"\Delta t \cdot r'_x(t^*_i)", r"\right)","^2", "+", r"\left(", r"\Delta t \cdot r'_y(t^*_i)", r"\right)","^2","}").set_color(
            GREEN).next_to(parafunc, direction=UP)
        temp[1:-1].set_color(BLUE)
        self.eqs.append((temp, [
            [0,1,2,None, None, None, "3f","4f",5,6, None, None, None, "7f","8f",9],
            [0,1,3,  2,    4, 5, None,None,6,8, 7, 9, 10, None,None,5]
        ]))
        self.ntx += 1
        lns = transform_lines(14,True)

        MVT = Text("(MVT)").scale(1.5).next_to(temp)
        self.play(FadeIn(MVT))
        self.play(FadeOut(MVT))
        self.remove(MVT)
        self.wait(2)
        temp = MathTex(
            #     0              1         2            3          4          5          6    7                8   9       10              11         12      13     14        15           16     17
            r"\sum_{i=1}^n", r"\sqrt{", r"\left(", r"\Delta t", r"\right)", r"^2", r"\cdot", r"r'_x(t^*_i)", "^2", "+",
            r"\left(", r"\Delta t", r"\right)", r"^2", r"\cdot", r"r'_y(t^*_i)", "^2", "}").set_color(
            GREEN).next_to(parafunc, direction=UP)
        temp[1:-1].set_color(BLUE)
        self.eqs.append((temp, [
            [0, 1, 2, 3, 4, 5, None, None, "5c", 6, 7, 8, 9, 10, None, None, "10c", 11],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        ]))
        self.ntx += 1
        lns = transform_lines(20, True)
        self.play(ApplyMethod(self.eq0[3].set_color,RED),ApplyMethod(self.eq0[11].set_color,RED)) #3,11



        temp = MathTex(
            #      0            1            2          3    4      5            6        7           8
            r"\sum_{i=1}^n",r"\sqrt{", r"r'_x(t^*_i)", "^2", "+",r"r'_y(t^*_i)", "^2", r"}", r"\Delta t").set_color(
            GREEN).next_to(parafunc, direction=UP)
        temp[1:-1].set_color(PURPLE)
        temp[-1].set_color(RED)
        self.eqs.append((temp, [
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
            [0,1,None,8,None,None, None, 2, 3, 4, None, 8, None, None, None, 5, 6, 7]
        ]))
        self.ntx += 1
        lns = transform_lines(30,True)
        self.wait()

        temp = MathTex(
            #      0            1            2          3    4      5            6        7           8
            r"\bigintsss_a^b", r"\sqrt{", r"r'_x(t)", "^2", "+", r"r'_y(t)", "^2", r"}", r"\; \tu{d}t").set_color(
            GREEN).next_to(parafunc, direction=UP)
        temp[1:-1].set_color(PURPLE)
        temp[-1].set_color(RED)
        self.eqs.append((temp, [
            [x for x in range(9)],
            [x for x in range(9)]
        ]))
        self.ntx += 1
        lns = transform_lines(100, True)
        self.wait()



class Example(Scene):
    def construct(self):
        #              0    1   2   3   4   5   6
        eq0 = MathTex("x=", "a", "(", "b", "+", "c", ")")
        #              0    1       2   3   4   5
        eq1 = MathTex("x=", "a", "b", "+", "a", "c")

     #   eq1.align_to(eq0, UR)
        self.play(FadeIn(eq0))
        self.wait()
        transform_indexes = [
            [0, 1, "2f", 3, 4, "1c", 5, "6f"],
            #  | |      | |  |   |  |
            [0, 1, None, 2, 3, 4, 5, None],
        ]
        def getTexTransform(transform_indices):
                return [
                    Create(eq1[j]) if i is None else
                    ReplacementTransform(eq0[i], eq1[j]) if type(i) is not str and j is not None else
                    FadeOut(eq0[int(i[:-1])]) if i[-1] == "f" or j is None else
                    ReplacementTransform(eq0[int(i[:-1])].copy(), eq1[j], path_arc=90 * DEGREES)
                    for i, j in zip(*transform_indices)
                ]

        self.play(*getTexTransform(transform_indexes))

class ArcLength56(Scene):
    scale_factor = 1

    def vector_func(self, t):
        return np.array(
            [self.scale_factor * t, self.scale_factor * (2/3 * t**(3/2)), 0])

    def construct(self):
        curve = ParametricFunction(lambda t: self.vector_func(t), t_range=[0, 5]).set_color(
            RED)

        c = 2*(2**(1/3)) - 1
        curve2 = ParametricFunction(lambda t: self.vector_func(t), t_range=[0, c]).set_color(
            WHITE)

        d = Dot(self.vector_func(c),radius=DEFAULT_SMALL_DOT_RADIUS).set_color(GREEN)
        # Number plane
        npl = NumberPlane()

        txt = MathTex(2).next_to(curve2.get_midpoint(),direction=DOWN+RIGHT,buff=SMALL_BUFF)
        txt2 = MathTex(r"(?,?)").set_color(ORANGE).next_to(d,direction=RIGHT)
        r = txt.add_background_rectangle()
        txt2.add_background_rectangle()
        v = VGroup(npl,curve,curve2,d,txt,txt2)
        v.scale(1.7*sqrt(2)).shift(LEFT*2+DOWN*0.35)


        # Add to scene
        self.add(v)

class TriangleInequality(Scene):
    def construct(self):
        # Create a Number Plane
        number_plane = NumberPlane()

        # Define vectors a, b, and a + b
        a = Vector([2, 2, 0]).set_color(GREEN)
        b = Vector([2, -1, 0]).set_color(ORANGE)
        a_plus_b = Vector(a.get_end() + b.get_end()).set_color("#da70d6")

        # Move b vector to start at the end of a
        b.shift(a.get_end())

        # Create vector labels
        a_label = MathTex("\\vec{x}").next_to(a.get_center(), UP+LEFT,buff=0.15).set_color(GREEN)
        b_label = MathTex("\\vec{y}").next_to(b.get_center(), UP+RIGHT, buff = 0.15).set_color(ORANGE)
        sum_label = MathTex("\\vec{x} + \\vec{y}").next_to(a_plus_b.get_center(), DOWN, buff=0.15).set_color("#da70d6").add_background_rectangle().rotate(
            a_plus_b.get_angle())

        # Create the inequality in LaTeX
        inequality_tex = MathTex("|\\vec{x} + \\vec{y}|", "\\leq", "|\\vec{x}|", "+", "|\\vec{y}|")
        inequality_tex.set_color("#da70d6")
        inequality_tex[2].set_color(GREEN)
        inequality_tex[4].set_color(ORANGE)
        inequality = BackgroundRectangle(inequality_tex)
        inequality_group = VGroup(inequality, inequality_tex)
        inequality_group.move_to(2 * DOWN)

        # Create a group to scale everything up
        everything = VGroup(number_plane, a, b, a_plus_b, a_label, b_label, sum_label, inequality_group)
        everything.scale(1.414)

        # Add everything to the scene
        self.add(everything)

class Lp(Scene):
    def construct(self):
        npl = NumberPlane().scale(2)

        # Define the labels
        labels = [
            Tex("1").next_to(npl.c2p(1, 0), DOWN),
            Tex("-1").next_to(npl.c2p(-1, 0), DOWN),
            Tex("1").next_to(npl.c2p(0, 1), LEFT, buff=0.17),
            Tex("-1").next_to(npl.c2p(0, -1), LEFT, buff=0.17)
        ]

        # L2 Unit Ball (Circle)
      #  l2_ball = Circle(radius=2, color=RED, fill_opacity=0.4)
        t = ValueTracker(2)
        l2_ball = always_redraw(
            lambda: ImplicitFunction(lambda x, y: abs(x) ** t.get_value() + abs(y) ** t.get_value() - 1 if t.get_value() < 90 else
            max(abs(x),abs(y)) - 1
                                     , color=RED)
            .scale(2)
            .set_fill(RED, opacity=0.4)
            .set_stroke(width=3)  # You can adjust the stroke width to your liking
        )

       # def makeText():
        #    v = int(t.get_value()) if int(t.get_value()) == t.get_value() else round(t.get_value(),2)
         #   s = MathTex(r"|x|", "^{",v, "}+", r"|y|", "^{",v, "}=", "1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
          #  s[0].set_color(GREEN)
          #  s[1].set_color("#da70d6")
          #  s[3].set_color(ORANGE)
          #  s[4].set_color("#da70d6")
          #  return s
        #txt = always_redraw(makeText)
        txt = MathTex(r"x",r"^2", "+", r"y","^2",r"\leqslant","1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt[0].set_color(GREEN)
        txt[1].set_color("#da70d6")
        txt[3].set_color(GREEN)
        txt[4].set_color("#da70d6")

        txt1 = MathTex(r"|x|", r"^1", "+", r"|y|", "^1", "\leqslant", "1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt1[0].set_color(GREEN)
        txt1[1].set_color("#da70d6")
        txt1[3].set_color(GREEN)
        txt1[4].set_color("#da70d6")

        txt2 = MathTex(r"\max(","|x|",",","|y|",")", "\leqslant", "1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt2[0].set_color("#da70d6")
        txt2[1].set_color(GREEN)
        txt2[3].set_color(GREEN)
        bg1 = BackgroundRectangle(txt)
        adj = VGroup(npl, l2_ball,*labels, bg1, txt) #l2_ball
        self.add(adj)
        self.play(t.animate.set_value(1),TransformMatchingTex(txt,txt1),run_time=1)

        def genPoint(x):
           # print(1-abs(x))
            if t.get_value() > 90:
                if x > -1:
                    return 2
                return (2-abs(x+1))
            return 2*(1-(abs(x))**t.get_value())**(1/t.get_value())
        t1 = ValueTracker(1) # -1 0 1 top hemi
        t2 = ValueTracker(0)

        dot1 = Dot([2,0,0]).set_color(BLUE).add_updater(lambda d: d.move_to([-2 if t1.get_value() < -1 else (2*t1.get_value() if t1.get_value() <= 1 else 2*(2-t1.get_value())),genPoint(t1.get_value()) if t1.get_value() <= 1 else -genPoint(2 - t1.get_value()),0]))
        dot2 = Dot([0,2,0]).set_color(TEAL).add_updater(lambda d: d.move_to([-2 if t2.get_value() < -1 else (2*t2.get_value() if t2.get_value() <= 1 else 2*(2-t2.get_value())),genPoint(t2.get_value()) if t2.get_value() <= 1 else -genPoint(2 - t2.get_value()),0]))
        lne = always_redraw(lambda:
                            Line(dot1.get_center(),dot2.get_center()).set_color(YELLOW)
                            )
        self.play(Create(dot1),Create(dot2))
        self.play(Create(lne))

        self.wait()
        self.play(t1.animate.set_value(1.7),t2.animate.set_value(0.7),run_time=3)
        self.wait(0.6)

        self.play(AnimationGroup(t.animate.set_value(100), TransformMatchingTex(txt1, txt2), run_time=1), AnimationGroup(t1.animate.set_value(2.75),t2.animate.set_value(-1.66),run_time=4.3))



class LpLI(Scene):
    def construct(self):
        SHIFT = UP + 1.5*RIGHT
        npl = NumberPlane().scale(2)

        # Define the labels
        labels = [
            Tex("1").next_to(npl.c2p(1, 0), DOWN),
            Tex("-1").next_to(npl.c2p(-1, 0), DOWN),
            Tex("1").next_to(npl.c2p(0, 1), LEFT, buff=0.17),
            Tex("-1").next_to(npl.c2p(0, -1), LEFT, buff=0.17)
        ]

        # L2 Unit Ball (Circle)
        l2_ball = Circle(radius=2, color=RED, fill_opacity=0.4)
        t = ValueTracker(2)

        txt = MathTex(r"x",r"^2", "+", r"y","^2",r"\leqslant","1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt[0].set_color(GREEN)
        txt[1].set_color("#da70d6")
        txt[3].set_color(GREEN)
        txt[4].set_color("#da70d6")

        txt1 = MathTex(r"|x|", r"^1", "+", r"|y|", "^1", "\leqslant", "1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt1[0].set_color(GREEN)
        txt1[1].set_color("#da70d6")
        txt1[3].set_color(GREEN)
        txt1[4].set_color("#da70d6")

        txt2 = MathTex(r"\max(","|x|",",","|y|",")", "\leqslant", "1").scale(1.5).to_edge(UP, buff=MED_SMALL_BUFF + 0.05)
        txt2[0].set_color("#da70d6")
        txt2[1].set_color(GREEN)
        txt2[3].set_color(GREEN)
        bg1 = BackgroundRectangle(txt)
        adj = VGroup(npl, l2_ball,*labels) #l2_ball
        adj.shift(SHIFT)
        self.add(adj)

        def genPoint(x):
           # print(1-abs(x))
            if t.get_value() > 90:
                if x > -1:
                    return 2
                return (2-abs(x+1))
            return 2*(1-(abs(x))**t.get_value())**(1/t.get_value())
        t1 = ValueTracker(1.7) # -1 0 1 top hemi
        t2 = ValueTracker(0.7)

        dot1 = Dot(SHIFT+[-2 if t1.get_value() < -1 else (2*t1.get_value() if t1.get_value() <= 1 else 2*(2-t1.get_value())),genPoint(t1.get_value()) if t1.get_value() <= 1 else -genPoint(2 - t1.get_value()),0]).set_color(BLUE).add_updater(lambda d: d.move_to(SHIFT+[-2 if t1.get_value() < -1 else (2*t1.get_value() if t1.get_value() <= 1 else 2*(2-t1.get_value())),genPoint(t1.get_value()) if t1.get_value() <= 1 else -genPoint(2 - t1.get_value()),0]))
        dot2 = Dot(SHIFT+[-2 if t2.get_value() < -1 else (2*t2.get_value() if t2.get_value() <= 1 else 2*(2-t2.get_value())),genPoint(t2.get_value()) if t2.get_value() <= 1 else -genPoint(2 - t2.get_value()),0]).set_color(TEAL).add_updater(lambda d: d.move_to(SHIFT+[-2 if t2.get_value() < -1 else (2*t2.get_value() if t2.get_value() <= 1 else 2*(2-t2.get_value())),genPoint(t2.get_value()) if t2.get_value() <= 1 else -genPoint(2 - t2.get_value()),0]))
        lne = always_redraw(lambda:
                            Line(dot1.get_center(),dot2.get_center()).set_color(YELLOW)
                            )
        li = VGroup(dot1,dot2,lne)
        self.add(li)
        slider = Slider(range=[0, 1], labels={0:0,1:1})
        # {0:0,np.pi/2:MathTex(r"\f{\pi}{2}"),np.pi:MathTex(r"\pi")}
        slider_group = slider.slider_group.shift(UP)
        slider.change_vector_color(GREEN).change_text_col(GREEN)
        self.add(slider_group)
        interpPoint = dot1.copy().set_color(PURE_GREEN).scale(1.5)
        interpPoint.add_updater(lambda m: m.move_to(slider.t_tracker.get_value()*dot1.get_center() + (1-slider.t_tracker.get_value())*dot2.get_center()))
        self.play(Create(interpPoint))
        self.wait()
        self.play(
            slider.t_tracker.animate.set_value(slider.upper), run_time=6)
