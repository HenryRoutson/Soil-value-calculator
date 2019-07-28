import numpy as np

def run(ChangeVector,SubVectors): 

    """Create functions to be used"""

    def unitVector(Vector):
        # Vector / Vector Magnitude
        return Vector/np.linalg.norm(Vector)

    """Find best vector"""

    # Set variables
    MaxSimilarity = 0
    UnitChangeVector = unitVector(ChangeVector)

    # Test direction similarity for each
    for n in range(len(SubVectors)):
        Similarity = np.dot(UnitChangeVector,unitVector(SubVectors[n]))
        if MaxSimilarity<Similarity:
            MaxSimilarity = Similarity
            MaxVectorPos = n

    # Break if no vector can get closer
    if MaxSimilarity == 0:
        return None , None

    # return values of best vector to GUI
    # vector scale , vector 
    return int(MaxVectorPos), float(np.linalg.norm(ChangeVector)/np.linalg.norm(SubVectors[MaxVectorPos]))
    