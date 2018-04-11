from tqdm import tqdm


class MFC:

    def __init__(self, G, start):
        self.G = G
        self.start = start
        self.reference_dictionary = {start: 0}
        self.visited = [start]
        self.max_references = []
        self.i = 0
        self.last_max = 2
        self.local_max = (-1, 'None')

    def next(self):
        if not self.reference_dictionary.keys():
            return -1
        else:
            if self.local_max[0] > self.last_max:
                max_vertex = self.local_max[1]
            else:
                max_vertex = max(self.reference_dictionary, key=lambda i: self.reference_dictionary[i])

            max_ref = self.reference_dictionary[max_vertex]

            self.last_max = max_ref
            self.local_max = (-1, 'None')
            del self.reference_dictionary[max_vertex]

            for vertex in self.G[max_vertex]:
                degree = self.G.degree(vertex)
                # Update reference if it exists and has not been explored
                if vertex in self.visited and vertex in self.reference_dictionary:
                    updated_ref = (self.reference_dictionary[vertex] * degree) + 1.0
                    self.reference_dictionary[vertex] = updated_ref / degree

                    max_val = self.reference_dictionary[vertex]
                    if max_val >= self.last_max and max_val > self.local_max[0]:
                        self.local_max = (max_val, vertex)

                # Else give starting reference
                elif vertex not in self.visited:
                    ref_score = 1.0 / degree
                    self.reference_dictionary[vertex] = ref_score
                    self.visited.append(vertex)

            self.max_references.append(max_ref)
            self.i += 1

            return max_vertex

    def empty(self):
        return not self.reference_dictionary.keys()

    def communities(self, delta=0.5):
        self._reset()

        community_index = -1

        smin = 0.
        smax = 0.

        community_dict = {community_index: set()}
        last_ref = 0

        pbar = tqdm(desc="original-mfc calculating communities", unit="vertex")

        while not self.empty():
            current_max = self.next()
            current_ref = self.max_references.pop()

            if current_ref > smax:
                smax = current_ref
            elif current_ref < smin:
                smin = current_ref

            target_diff = (abs(smax - smin)) * delta

            if abs(current_ref - last_ref) > target_diff:
                community_index = current_max
                community_dict[community_index] = set()

            community_dict[community_index].add(current_max)

            last_ref = current_ref
            pbar.update()

        self._reset()
        pbar.close()
        return community_dict

    def _reset(self):
        self.reference_dictionary = {self.start: 0}
        self.visited = [self.start]
        self.max_references = []
        self.i = 0
