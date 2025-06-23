
from manim import *
import networkx as nx
import numpy as np

class ErdosRenyiGraph(Scene):
    def construct(self):
        # text list
        announcement = Text("Referenties")
        ref_01 = Text("Spencer N. Axani. The Physics Behind the CosmicWatch Desktop Muon Detectors", font_size =30)
        ref_02 = Text("Cosmic ray. Wikipedia", font_size =30)
        ref_03 = Text ("Scintillator. Wikipedia", font_size =30)
        ref_04 = Text("Photomultiplier Tubes: an overview. Science Direct Topics", font_size =30)
        # Create a NetworkX random graph (example)
        nxgraph = nx.erdos_renyi_graph(n=15, p=0.3)

        # Assign random colors to nodes
        vertex_colors = {
            v: random_bright_color()
            for v in nxgraph.nodes
        }

        # Optional: Assign colors to edges
        edge_colors = {
            (u, v): random_bright_color()
            for u, v in nxgraph.edges
        }

        # Create the Manim graph
        G = Graph.from_networkx(
            nxgraph,
            layout="spring",
            layout_scale=3.5,
            vertex_config={
                v: {"fill_color": vertex_colors[v]} for v in nxgraph.nodes
            },
            edge_config={
                (u, v): {"stroke_color": edge_colors[(u, v)]}
                for u, v in nxgraph.edges
            }
        )

        self.play(Create(G))
        self.play(Write(announcement))
        # Animate nodes moving into a circular shape
        self.play(*[
            G[v].animate.move_to(
                5 * RIGHT * np.cos(ind / 7 * PI) +
                3 * UP * np.sin(ind / 7 * PI)
            )
            for ind, v in enumerate(G.vertices)
        ])

        self.wait(1)
        
        self.play(Uncreate(G))

        # text moving up, references appearing
        self.play(announcement.animate.shift(3*UP))

        self.add(ref_01)
        
        
        self.play(ref_01.animate.shift(2 *UP))

        self.add(ref_02)

       
        self.play(ref_02.animate.shift(UP))

        self.add(ref_03)
        self.play(ref_03.animate.shift(0*UP))
        
       

        self.add(ref_04)
        self.play(ref_04.animate.shift(DOWN))