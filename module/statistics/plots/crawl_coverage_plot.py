import matplotlib.pyplot as plt
from queue import Queue
from random import choice
import copy

import time

from tqdm import tqdm

from module.crawling.opic import OPIC


# TODO plot size of communities found

class CrawlCoverage:

    def coverage_plot(self, graph, communities, memberships):
        number_communities = len(communities.keys())
        plt.axis([0, number_communities, 0, 100])

        random_start = choice(list(graph.nodes))
        print("Starting process from vertex: %s" % random_start)

        bfs = copy.deepcopy(communities)
        opic = copy.deepcopy(communities)
        dfs = copy.deepcopy(communities)
        mfc = copy.deepcopy(communities)

        self.bfs(graph, bfs, memberships.copy(), random_start)
        self.dfs(graph, dfs, memberships.copy(), random_start)
        self.mfc(graph, mfc, memberships.copy(), random_start)
        self.opic(graph, opic, memberships.copy(), random_start)

        plt.ylabel("Percentage of nodes traversed")
        plt.xlabel("Communities fully traversed")

    @staticmethod
    def opic(graph, opic_communities, opic_members, start):
        x, y = [], []

        nodes = list(graph.nodes)
        number_nodes = len(nodes)
        visited = 0.0
        community_explored = 0
        opic = OPIC(graph)

        pbar = tqdm(total=number_nodes, desc="opic crawling", unit='vertex')

        opic.visit(start)
        nodes.remove(start)
        pbar.update()
        visited += 1.0

        communities_incremented = CrawlCoverage._community_removed(start, opic_communities, opic_members)
        community_explored += communities_incremented

        x.append(community_explored)
        y.append(visited / number_nodes)

        while nodes:
            max_cash_node = opic.local_max_vertex
            opic.visit(max_cash_node)

            if max_cash_node in nodes:
                nodes.remove(max_cash_node)
                pbar.update()

                communities_incremented = CrawlCoverage._community_removed(max_cash_node, opic_communities,
                                                                           opic_members)
                community_explored += communities_incremented

                visited += 1
                x.append(community_explored)
                y.append((visited / number_nodes) * 100)


        pbar.close()

        plt.plot(x, y, linewidth=2, label="opic")

    @staticmethod
    def bfs(graph, bfs_communities, bfs_members, start):
        x, y = [], []
        community_explored, nodes_explored = 0, 0

        queue = Queue()
        visited = set()
        # Add first node
        queue.put(start)
        visited.add(start)

        pbar = tqdm(total=len(graph.nodes), desc="bfs crawling", unit='vertex')

        while queue.not_empty:
            if len(visited) > len(graph.nodes):
                print("Something went wrong")
                break
            if queue.empty():
                break
            u = queue.get()

            communities_incremented = CrawlCoverage._community_removed(u, bfs_communities, bfs_members)
            community_explored += communities_incremented
            nodes_explored += 1.0

            y.append((nodes_explored / len(graph.nodes)) * 100)
            x.append(community_explored)
            for vertex in graph[u]:
                if vertex not in visited:
                    queue.put(vertex)
                    visited.add(vertex)

            pbar.update()

        pbar.close()
        plt.plot(x, y, linewidth=2, label="bfs")

    @staticmethod
    def dfs(graph, dfs_communities, dfs_members, start):
        x, y = [], []
        stack = []
        community_explored, nodes_explored = 0, 0

        visited = set()
        visited.add(start)
        stack.append(start)

        pbar = tqdm(total=len(graph.nodes), desc="dfs crawling", unit='vertex')

        while stack:
            u = stack.pop()
            nodes_explored += 1

            communities_incremented = CrawlCoverage._community_removed(u, dfs_communities, dfs_members)
            community_explored += communities_incremented

            y.append(nodes_explored / len(graph.nodes) * 100)
            x.append(community_explored)

            for vertex in graph[u]:
                if vertex not in visited:
                    visited.add(vertex)
                    stack.append(vertex)

            pbar.update()

        pbar.close()
        plt.plot(x, y, linewidth=2, label="dfs")

    @staticmethod
    def mfc(graph, mfc_communities, mfc_members, start):
        x, y = [], []
        community_explored, nodes_explored = 0, 0
        reference_dictionary = {}

        pbar = tqdm(total=len(graph.nodes), desc="mfc crawling", unit='vertex')

        visited = set()
        # Add first node
        reference_dictionary[start] = 0
        visited.add(start)
        local_max = (-1, '-1')
        last_max = 2

        while reference_dictionary.keys():
            if local_max[0] > last_max:
                _, max_vertex = local_max
            else:
                max_vertex = max(reference_dictionary, key=lambda i: reference_dictionary[i])

            last_max = reference_dictionary[max_vertex]

            del reference_dictionary[max_vertex]

            communities_incremented = CrawlCoverage._community_removed(max_vertex, mfc_communities, mfc_members)

            community_explored += communities_incremented
            nodes_explored += 1.0

            y.append((nodes_explored / len(graph.nodes)) * 100)
            x.append(community_explored)

            visited.add(max_vertex)
            local_max = (-1, '0')
            for vertex in graph[max_vertex]:
                degree = graph.degree(vertex)
                # Update reference if it exists and has not been explored
                if vertex in visited and vertex in reference_dictionary:
                    updated_ref = (reference_dictionary[vertex] * degree) + 1.0
                    reference_dictionary[vertex] = updated_ref / degree

                    if reference_dictionary[vertex] >= last_max and reference_dictionary[vertex] > local_max[0]:
                        local_max = (reference_dictionary[vertex], vertex)

                # Else give starting reference
                elif vertex not in visited:
                    ref_score = 1.0 / degree
                    reference_dictionary[vertex] = ref_score
                    visited.add(vertex)
            pbar.update()

        pbar.close()

        plt.plot(x, y, linewidth=2, label="mfc")

    @staticmethod
    def _community_removed(vertex, communities, members):
        number_empty = 0
        vertex = str(vertex)

        for community in members.get(vertex, []):
            communities[community].remove(vertex)

            if not communities[community]:
                number_empty += 1

        return number_empty
