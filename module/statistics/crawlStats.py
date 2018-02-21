import matplotlib.pyplot as plt
from queue import Queue
from random import choice
import copy

import time

from module.crawling.OPIC import OPIC


# TODO plot size of communities found

class CrawlStats:

    def __init__(self):
        plt.ylabel("Percentage of nodes traversed")
        plt.xlabel("Communities fully traversed")

    def coverage_plot(self, graph, communities, memberships):
        number_communities = len(communities.keys())

        print(number_communities)


        plt.axis([0, number_communities, 0, 100])

        random_start = choice(list(graph.nodes))
        print("Start: %s" % random_start)

        start_time = time.time()

        bfs = copy.deepcopy(communities)
        opic = copy.deepcopy(communities)
        dfs = copy.deepcopy(communities)
        mfc = copy.deepcopy(communities)
        random = copy.deepcopy(communities)
        #self.random_walk(graph, random, memberships.copy(), random_start)
        self.OPIC(graph, opic, memberships.copy(), random_start)
        self.MFC(graph, mfc, memberships.copy(), random_start)
        self.BFS(graph, bfs, memberships.copy(), random_start)
        self.DFS(graph, dfs, memberships.copy(), random_start)
        end_time = time.time()
        print("Total time %s" % (end_time - start_time))
        plt.legend()
        plt.show()

    @staticmethod
    def OPIC(G, opic_communities, opic_members, start):
        print("OPIC running...")
        x,y = [], []

        nodes = list(G.nodes)
        number_nodes = len(nodes)
        visited = 0.0
        community_explored = 0
        opic = OPIC(G, 40)

        opic.visit(start)
        nodes.remove(start)
        visited += 1.0

        communities_incremented = CrawlStats.community_removed(start, opic_communities, opic_members)
        community_explored += communities_incremented

        x.append(community_explored)
        y.append(visited / number_nodes)

        while nodes:
            #max_cash_node = max(opic.cash_current, key=lambda i: opic.cash_current[i])
            max_cash_node = opic.local_max_vertex
            opic.visit(max_cash_node)

            if max_cash_node in nodes:
                nodes.remove(max_cash_node)

                communities_incremented = CrawlStats.community_removed(max_cash_node, opic_communities, opic_members)
                if (communities_incremented + community_explored) > community_explored:
                    print("OPIC Explored %s percent" % ((visited / number_nodes) * 100 ))
                community_explored += communities_incremented

                visited += 1
                x.append(community_explored)
                y.append((visited / number_nodes) * 100)

        plt.plot(x, y, linewidth=2, label="OPIC")

    @staticmethod
    def BFS(G, bfs_communities, bfs_members, start):
        x, y = [], []
        community_explored, nodes_explored = 0, 0

        queue = Queue()
        visited = []
        # Add first node
        queue.put(start)
        visited.append(start)

        while queue.not_empty:
            if len(visited) > len(G):
                print("Something went wrong")
                break
            if queue.empty():
                break
            u = queue.get()

            communities_incremented = CrawlStats.community_removed(u, bfs_communities, bfs_members)
            if (communities_incremented + community_explored) > community_explored:
                print("BFS Explored %2.f percent" % ((nodes_explored / len(G.nodes)) * 100 ))
            community_explored += communities_incremented
            nodes_explored += 1.0

            y.append((nodes_explored / len(G.nodes)) * 100)
            x.append(community_explored)
            for vertex in G[u]:
                if vertex not in visited:
                    queue.put(vertex)
                    visited.append(vertex)

        plt.plot(x, y, linewidth=2, label="BFS")

    @staticmethod
    def random_walk(G, random_communities, random_members, start):
        print("Random walk running")
        x, y = [], []
        community_explored, nodes_explored = 0, 0

        queue = []
        visited = []
        # Add first node
        queue.append(start)
        visited.append(start)

        while queue:
            if not queue:
                break

            u = choice(queue)
            queue.remove(u)

            communities_incremented = CrawlStats.community_removed(u, random_communities, random_members)
            community_explored += communities_incremented
            nodes_explored += 1.0

            y.append((nodes_explored / len(G.nodes)) * 100)
            x.append(community_explored)
            for vertex in G[u]:
                if vertex not in visited:
                    queue.append(vertex)
                    visited.append(vertex)

        plt.plot(x, y, linewidth=2, label="Random")

    @staticmethod
    def DFS(G, dfs_communities, dfs_members, start):
        print("DFS running")
        x, y = [], []
        stack = []
        community_explored, nodes_explored = 0, 0

        visited = set()
        visited.add(start)
        stack.append(start)

        while stack:
            u = stack.pop()
            nodes_explored += 1

            communities_incremented = CrawlStats.community_removed(u, dfs_communities, dfs_members)
            community_explored += communities_incremented

            y.append(nodes_explored / len(G.nodes) * 100)
            x.append(community_explored)

            for vertex in G[u]:
                if vertex not in visited:
                    visited.add(vertex)
                    stack.append(vertex)

        plt.plot(x, y, linewidth=2, label="DFS")

    @staticmethod
    def MFC(G, mfc_communities, mfc_members, start):
        x, y = [], []
        community_explored, nodes_explored = 0, 0
        reference_dictionary = {}

        visited = []
        # Add first node
        reference_dictionary[start] = 0
        visited.append(start)

        while reference_dictionary.keys():
            max_vertex = max(reference_dictionary, key=lambda i: reference_dictionary[i])
            del reference_dictionary[max_vertex]

            communities_incremented = CrawlStats.community_removed(max_vertex, mfc_communities, mfc_members)

            if (communities_incremented + community_explored) > community_explored:
                print("MFC Explored %2.f percent" % ((nodes_explored / len(G.nodes)) * 100 ))

            community_explored += communities_incremented
            nodes_explored += 1.0

            y.append((nodes_explored / len(G.nodes)) * 100)
            x.append(community_explored)

            for vertex in G[max_vertex]:
                degree = G.degree(vertex)
                # Update reference if it exists and has not been explored
                if vertex in visited and vertex in reference_dictionary:
                    updated_ref = (reference_dictionary[vertex] * degree) + 1.0
                    reference_dictionary[vertex] = updated_ref / degree
                # Else give starting reference
                elif vertex not in visited:
                    ref_score = 1.0 / degree
                    reference_dictionary[vertex] = ref_score
                    visited.append(vertex)

        plt.plot(x, y, linewidth=2, label="MFC")

    @staticmethod
    def community_removed(vertex, communities, members):
        number_empty = 0

        for community in members.get(vertex, []):
            # TODO May have already been removed
            communities[community].remove(vertex)

            if not communities[community]:
                number_empty += 1

        return number_empty
