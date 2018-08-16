import os
import cv2
import glob
import json
from classifier import Panorama


class FeatureDatabase:

    def __init__(self, descriptor, data_dir):
        """Describes all images in data_dir and loads ground_truth.json as scenes"""
        self.descriptor = descriptor
        self.scenes = None
        self._index(data_dir)

    def _index(self, data_dir):
        """Indexes the database with the descriptor"""
        features = {}
        for path in glob.glob(os.path.join(data_dir, '*')):
            if path.endswith('.json'):
                with open(path) as f:
                    self.scenes = set(Panorama(comp) for comp in json.load(f))
                continue
            img_fname = os.path.split(path)[-1]
            img = cv2.imread(path)
            features[img_fname] = self.descriptor.describe(img)
        self.features = features

    def query(self, query_feats, limit=10):
        distances = {}
        for img_fname, img_feats in self.features.items():
            distances[img_fname] = query_feats.distance(img_feats)
        # sort results by distance (lower distance is more similar to the query)
        yield from sorted(distances.items(), key=lambda kv: kv[-1])[:limit]

