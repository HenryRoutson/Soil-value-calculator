__author__  = "Henry Routson"
__date__ = "2019-08-30"

import numpy as np

"""Create functions to be used"""

def unitvector(vector):
    # np.linalg.norm is vector scale
    vector_magnitude = np.linalg.norm(vector)
    if vector_magnitude == 0.0:
        return vector
    return vector / vector_magnitude

def run(change_vector,subvectors): 

    """Find best vector"""

    # Set variables
    max_similarity = 0.0

    # Test direction similarity for each
    for n, subvector in enumerate(subvectors):
        similarity = np.dot(unitvector(change_vector),unitvector(subvector))
        # and find the most similar
        if max_similarity < similarity:
            max_similarity = similarity
            max_vector_pos = n

    # Break if there isn't a vector in change_vectors direction
    if max_similarity == 0.0:
        return False , False

    # returns the best vector to GUI, (index, scale)
    # the scale makes the subvector scale equal the change_vector scale, which makes them as close as they can be
    return max_vector_pos, np.linalg.norm(change_vector) / np.linalg.norm(subvectors[max_vector_pos])
    