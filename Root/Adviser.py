import numpy as np

"""Create functions to be used"""

def unitVector(Vector):
    Vector_Magnitude = np.linalg.norm(Vector)
    if Vector_Magnitude == 0:
        return Vector
    return Vector / Vector_Magnitude

def run(ChangeVector,SubVectors): 

    """Find best vector"""

    # Set variables
    MaxSimilarity = 0

    # Test direction similarity for each
    for n, SubVector in enumerate(SubVectors):
        Similarity = np.dot(unitVector(ChangeVector),unitVector(SubVector))
        if MaxSimilarity<Similarity:
            MaxSimilarity = Similarity
            MaxVectorPos = n

    # Break if there isn't a vector in changeVectors direction
    if MaxSimilarity == 0:
        return None , None

    # return values of best vector to GUI
    # vector, vector scale
    return MaxVectorPos, np.linalg.norm(ChangeVector) / np.linalg.norm(SubVectors[MaxVectorPos])
    