from string import Template


system_prompt = Template("/n".join([
    "you are a helpful assistant that answers questions based on the provided context.",
    "You will be provided with a context and a question.",
    "Your task is to extract relevant information from the context to answer the question.",
    "If the context does not contain enough information to answer the question, respond with 'I don't know'.",
    "If the context contains information that is not relevant to the question, ignore it.",
    "You should not make up any information."
    ]))

doc_prompt = Template("/n".join([
    "Document number: $doc_num",
    "Document content: $doc_content"
    ]))

footer_prompt = Template("/n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "Question:",
    "$query",
    "",
    "Answer:"
    ]))

