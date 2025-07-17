from enum import Enum
class Processingextension(Enum):
    """
    Enum for processing extensions.
    """
    CSV = ".csv"
    JSON = ".json"
    XML = ".xml"
    TXT = ".txt"
    PDF = ".pdf"
    def __str__(self):
        return self.value
