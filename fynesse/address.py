# This file contains code for suporting addressing questions in the data
import numpy as np
from geopy.distance import distance
import osmnx as ox
"""# Here are some of the imports we might expect 
import sklearn.model_selection  as ms
import sklearn.linear_model as lm
import sklearn.svm as svm
import sklearn.naive_bayes as naive_bayes
import sklearn.tree as tree

import GPy
import torch
import tensorflow as tf

# Or if it's a statistical analysis
import scipy.stats"""

"""Address a particular question that arises from the data"""

# Use this box for any code you need
def getBoundingBox(location, side_length_km):
  """Returns the northeastern point of the bounding box (numerically larger) and the southwestern point (numerically smaller).
  Doesn't hold true if the side_length gets too big."""
  northeast_point = distance(side_length_km/np.sqrt(2)).destination(location, bearing=45)
  southwest_point = distance(side_length_km/np.sqrt(2)).destination(location, bearing=180+45) # I found out about this series of function calls online
  return (northeast_point.latitude, northeast_point.longitude), (southwest_point.latitude, southwest_point.longitude)

def count_pois_near_coordinates(latitude: float, longitude: float, tags: dict, distance_km: float = 1.0) -> dict:
    """
    Count Points of Interest (POIs) near a given pair of coordinates within a specified distance.
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        tags (dict): A dictionary of OSM tags to filter the POIs (e.g., {'amenity': True, 'tourism': True}).
        distance_km (float): The distance around the location in kilometers. Default is 1 km.
    Returns:
        dict: A dictionary where keys are the OSM tags and values are the counts of POIs for each tag.
    """
    # ChatGPT told me that I could use geopy to get the distance between two points specified by coordinates, and gave me an example that I used.
    # kmPerDegree = 111
    (north, east), (south,west) = getBoundingBox((latitude, longitude), distance_km*2)
    places_of_interest = ox.geometries_from_bbox(north, south, east, west, tags)
    origin = (latitude, longitude)
    isWithinDistance = lambda row : distance(origin, (row.geometry.centroid.x, row.geometry.centroid.y)).km < distance_km
    return len(places_of_interest[isWithinDistance])

if __name__ == "__main__":
  print("Test")
  print(getBoundingBox((0,0), 222)) # expect to see (1,1), (-1,-1)
  print(getBoundingBox((60,16), 222)) # expect to see (61,18), (59,14)
  # ((1.0037980684640913, 0.9972313173423671), (-1.0037980684640913, -0.9972313173423671))
  # ((60.98073503140397, 18.050462434827125), (58.98913187102387, 14.06917263719269)) 
