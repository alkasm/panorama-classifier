import networkx as nx


class Panorama(frozenset): pass


class PanoramaClassifier:

    def __init__(self, thresh=1.25):
        self.epsilon = thresh

    def classify(self, db):
        G = nx.Graph()
        for img_fname, feats in db.features.items():
            for result_fname, score in db.query(feats):
                G.add_edge(img_fname, result_fname, similarity=score)
        G2 = nx.Graph([(u, v, data) for u, v, data in G.edges(data=True)
                      if data['similarity'] < self.epsilon])
        panoramas = set(Panorama(comp) for comp in nx.connected_components(G2))
        return panoramas

