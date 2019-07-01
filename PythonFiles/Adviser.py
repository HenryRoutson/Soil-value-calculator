def run(MainVector,CurrentPos,SubVectors):

    import numpy as np

    """Create functions to be used"""

    def unitVector(Vector):
        # Vector / Vector Magnitude
        return Vector/np.linalg.norm(Vector)

    """Find best vector"""

    # Set variables
    MaxSimilarity = 0
    GOALVECTOR = MainVector-CurrentPos
    UNITGOALVECTOR = unitVector(GOALVECTOR)

    # Test direction similarity for each
    for n in range(len(SubVectors)):
        Similarity = np.dot(UNITGOALVECTOR,unitVector(SubVectors[n]))
        if MaxSimilarity<Similarity:
            MaxSimilarity = Similarity
            MaxVectorPos = n

    # Break if no vector can get closer
    if MaxSimilarity==0:
        exit()

    # return values of best vector to GUI
    # vector scale , vector 
    return float(np.linalg.norm(GOALVECTOR)/np.linalg.norm(SubVectors[MaxVectorPos])) , MaxVectorPos