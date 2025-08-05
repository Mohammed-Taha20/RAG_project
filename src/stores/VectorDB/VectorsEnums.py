from enum import Enum

class VectorDBenum(Enum):
    VectorDB = "QDRANT"

class DistanceMetricEnum(Enum):
    EUCLIDEAN = "euclidean"
    COSINE = "cosine"
