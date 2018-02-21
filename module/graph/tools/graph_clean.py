import networkx as nx


class GraphClean():

    @staticmethod
    def prune_unconnected_components(graph):
        current = graph
        # Remove self loops
        for vertex in graph.nodes_with_selfloops():
            graph.remove_edge(vertex, vertex)

        if not nx.is_connected(graph):
            connected_subgraphs = nx.connected_component_subgraphs(graph)
            current = next(connected_subgraphs)

            for sub_graph in connected_subgraphs:
                if len(sub_graph.nodes) > len(current.nodes):
                    current = sub_graph

        return current
