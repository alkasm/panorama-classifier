import argparse
import os
from cbir import HistogramDescriptor, FeatureDatabase
from classifier import PanoramaClassifier


def classify(data_dir, thresh):
    descriptor = HistogramDescriptor()
    classifier = PanoramaClassifier(thresh=thresh)
    db = FeatureDatabase(descriptor, data_dir)
    scenes = classifier.classify(db)
    if db.scenes:
        print('Ground truth:', db.scenes)
        print('Found scenes:', scenes)
        print('Correct classification:', scenes == db.scenes)
    else:
        print('Found scenes:', scenes)
        print('ground_truth.json not found in', data_dir, 'for evaluation.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('data',
        help='directory with panoramic images')
    parser.add_argument('--thresh', default=1.25,
        help='threshold for matching')
    args = parser.parse_args()

    classify(args.data, args.thresh)

