import matplotlib.pyplot as plt


class MFC:

    def __init__(self, G, start):
        self.G = G
        self.reference_dictionary = {start: 0}
        self.visited = [start]
        self.x,self.y = [], []
        self.i = 0

    def next(self):
        if not self.reference_dictionary.keys():
            return -1
        else:
            max_vertex = max(self.reference_dictionary, key=lambda i: self.reference_dictionary[i])
            max_ref = self.reference_dictionary[max_vertex]
            del self.reference_dictionary[max_vertex]

            for vertex in self.G[max_vertex]:
                degree = self.G.degree(vertex)
                # Update reference if it exists and has not been explored
                if vertex in self.visited and vertex in self.reference_dictionary:
                    updated_ref = (self.reference_dictionary[vertex] * degree) + 1.0
                    self.reference_dictionary[vertex] = updated_ref / degree
                # Else give starting reference
                elif vertex not in self.visited:
                    ref_score = 1.0 / degree
                    self.reference_dictionary[vertex] = ref_score
                    self.visited.append(vertex)

            self.x.append(self.i)
            self.y.append(max_ref)
            self.i += 1

            return max_vertex

    def empty(self):
        return not self.reference_dictionary.keys()

    def plot(self):
        plt.plot(self.x, self.y, linewidth=2.0)
        #plt.show()
