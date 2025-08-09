from enum import Enum
class LLMenum(Enum):
    Groq = "Groq"
    Cohere = "COHERE"
    CohereEmbedding = "COHERE_EMBED"

class LLMenumGroq(Enum):
    System = "system"
    User = "user"

class LLMenumCohere(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    search_doc="search_document"
    search_query="search_query"

class LLMenumDocumentType(Enum):
    doc="document"
    query="query"