import sys
import types
import numpy as np

class MockAnnoyIndex:
    def __init__(self, f, metric):
        self.f = f
        self.metric = metric
        self.items = {}

    def add_item(self, i, vector):
        self.items[i] = np.array(vector)

    def build(self, n_trees):
        pass

    def get_nns_by_vector(self, vector, n, include_distances=False):
        query = np.array(vector)
        results = []
        for i, vec in self.items.items():
            # Calculate cosine similarity
            dot = np.dot(query, vec)
            norm_q = np.linalg.norm(query)
            norm_v = np.linalg.norm(vec)
            sim = dot / (norm_q * norm_v + 1e-9)
            # In Annoy, angular distance is roughly 2 * (1 - sim)
            dist = 2.0 * (1.0 - sim)
            results.append((i, dist))
        
        # Sort by distance ascending (closest first)
        results.sort(key=lambda x: x[1])
        top_n = results[:n]
        
        if include_distances:
            indices = [x[0] for x in top_n]
            distances = [x[1] for x in top_n]
            return indices, distances
        else:
            return [x[0] for x in top_n]

def register_mock_annoy():
    annoy_mock = types.ModuleType("annoy")
    annoy_mock.AnnoyIndex = MockAnnoyIndex
    sys.modules["annoy"] = annoy_mock
