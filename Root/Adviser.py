import numpy as np

def run(ChangeVector,SubVectors): 

    """Create functions to be used"""

    def unitVector(Vector):
        Vector_Magnitude = np.linalg.norm(Vector)
        if Vector_Magnitude == 0:
            return Vector
        return Vector / Vector_Magnitude

    """Find best vector"""

    # Set variables
    MaxSimilarity = 0
    UnitChangeVector = unitVector(ChangeVector)

    # Test direction similarity for each
    for n, SubVector in enumerate(SubVectors):
        Similarity = np.dot(UnitChangeVector,unitVector(SubVector))
        if MaxSimilarity<Similarity:
            MaxSimilarity = Similarity
            MaxVectorPos = n

    # Break if no vector can get closer
    if MaxSimilarity == 0:
        return None , None

    # return values of best vector to GUI
    # vector scale , vector 
    return int(MaxVectorPos), float(np.linalg.norm(ChangeVector)/np.linalg.norm(SubVectors[MaxVectorPos]))
    