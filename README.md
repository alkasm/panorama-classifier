This repo contains some modules and scripts to classify sets of images that belong together in a panorama. 

## Installation

1. Install Python 3.6+ (https://www.python.org) and `pipenv`

       $ pip install pipenv

1. Clone this repo

       $ git clone https://github.com/alkasm/panorama-classifier.git
    
1. Change directories into this repo

       $ cd panorama-classifier
       panorama-classifier $ 
    
1. Install the necessary packages from the `Pipfile` (`opencv-python` and `networkx` and their dependencies)

       panorama-classifier $ pipenv install
    
1. To run any scripts inside this environment, simply use `pipenv` as you normally would

       panorama-classifier $ pipenv run python classify_hist.py --help
    
## Usage

To classify panoramas based on their color histograms, you can use the `classify_hist.py` script and provide a folder containing images.

    panorama-classifier $ pipenv run python classify_hist.py --help
    
    usage: classify_hist.py [-h] [--thresh THRESH] data

    positional arguments:
      data             directory with panoramic images

    optional arguments:
      -h, --help       show this help message and exit
      --thresh THRESH  threshold for matching
      
Here the directory containing images expects there to only be two types of files: image files and an optional `.json` file for ground truth data to be compared against the classification. Aside from a `.json` file, all other files in the folder are presumed to be able to be read and opened by OpenCV. An optional argument `--thresh THRESH` can be passed to the script to override the default threshold of 1.25. 

## cbir Module

From [Wikipedia](https://en.wikipedia.org/wiki/Content-based_image_retrieval):

> Content-based image retrieval (CBIR), also known as query by image content (QBIC) and content-based visual information retrieval (CBVIR) is the application of computer vision techniques to the image retrieval problem, that is, the problem of searching for digital images in large databases. ...
>
> "Content-based" means that the search analyzes the contents of the image rather than the metadata such as keywords, tags, or descriptions associated with the image. The term "content" in this context might refer to colors, shapes, textures, or any other information that can be derived from the image itself. 

The `cbir` module contains two main pieces: the image content descriptors, and the database used for image retrieval. 

### Content descriptors

For the descriptors, `descriptors.py` defines some interfaces (`Features` and `Descriptor`) which can be subclassed to be used for the CBIR system, depending on how you want your images described and what distance metric should be used between features. Currently, the module has a `HistogramDescriptor` implemented which returns `HistogramFeatures` that can be compared with their `distance()` method, which uses the chi-squared distance metric to measure the distance between two histograms.

### Image Retrieval

For a reverse image search, the database needs to be initialized with the data and queryable. The `FeatureDatabase` inside `featuredb.py` is just a simple class to hold an instance of the indexed database in memory, with a query method. Any descriptor following the prototypes can be used here. The databases will be expanded out to allow actual database clients in the future (probably Redis for an in-memory database, SQLite for an on-disk database).

## classifier Module

The classifier recognizes panoramas by computing pairwise distances between each pair of image descriptors in the database. This defines a graph where each edge is weighted by the distance between two images. Thresholding this graph on the edge weights will keep only the strongest matches around, and the connected components in this thresholded graph correspond to the individual panoramas in the dataset. This module uses `networkx` to define the graph and run connected components on the result.

This classifier is loosely based on Brown and Lowe's 2003 paper [Recognising Panoramas](http://matthewalunbrown.com/papers/iccv2003.pdf) in ICCV, without the probablistic machinery used in the paper.

# References

1. R. Szeliski, [Image Alignment and Stitching: A Tutorial](https://www.microsoft.com/en-us/research/publication/image-alignment-and-stitching-a-tutorial/), Microsoft Research, 2004.

1. M. Brown, D. Lowe, [Recognising Panoramas](http://matthewalunbrown.com/papers/iccv2003.pdf), ICCV, 2003.
