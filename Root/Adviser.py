import numpy as np

"""Create functions to be used"""

def unitvector(vector):
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
        if max_similarity < similarity:
            max_similarity = similarity
            max_vector_pos = n

    # Break if there isn't a vector in change_vectors direction
    if max_similarity == 0.0:
        return False , False

    # return values of best vector to GUI
    # vector, vector scale
    return max_vector_pos, np.linalg.norm(change_vector) / np.linalg.norm(subvectors[max_vector_pos])
    