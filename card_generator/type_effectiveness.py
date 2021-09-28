import plotly.graph_objects as go
import networkx as nx
from pyvis.network import Network

from config import TYPE_CHART, IMMUNE, RESIST, REGULAR, WEAK

EFFECTIVENESS = {IMMUNE: 0, RESIST: 0.5, REGULAR: 1, WEAK: 2}


def run():
    graph = Network(height='1000px', width='1000px', directed=True)
    graph.barnes_hut()
    graph.add_nodes(TYPE_CHART.keys())
    for attacking_type in TYPE_CHART:
        for weak_type in TYPE_CHART[attacking_type][WEAK]:
            score = 2
            if attacking_type in TYPE_CHART[weak_type][RESIST]:
                score += 1
            elif attacking_type in TYPE_CHART[weak_type][IMMUNE]:
                score += 2
            print(attacking_type, weak_type, score)
            if score >= 3:
                graph.add_edge(attacking_type, weak_type)

    graph.show('type_effectiveness.html')


if __name__ == '__main__':
    run()
