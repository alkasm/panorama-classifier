import cv2
import numpy as np


class Descriptor:
    """Used to create feature descriptors."""

    def describe(self, img):
        """Describes an image by its features.
        
        Parameters
        ----------
        img : np.ndarray
            The image to be described
        
        Returns
        -------
        features : Features
            List-like type of doubles representing the features, with a
            distance method to get distance between two features.
        """
        raise NotImplementedError


class Features(list):
    """List-like features with a distance() method to find feature distance."""

    def distance(self, other):
        """Calculates the distance between two features."""
        raise NotImplementedError


class HistogramDescriptor(Descriptor):
    """Describes images by their HSV histograms."""
    
    def __init__(self, bins=(8, 12, 3)):
        self.bins = bins
 
    def describe(self, img):  
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([img], [0, 1, 2], None, self.bins,
                            [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, None).flatten()
        return HistogramFeatures(hist)


class HistogramFeatures(Features):
    """Utilizes chi^2 to measure the distance between two histograms."""

    def distance(self, other):
        hist_1, hist_2 = np.array(self), np.array(other)
        num = (hist_1 - hist_2)**2
        den = hist_1 + hist_2
        return 0.5 * np.sum(num[den!=0] / den[den!=0])

