# chat
from QWEN import ChatQWEN
from langchain_core.prompts import ChatPromptTemplate

# db related
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chromadb/"

# free model
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"


def load_db():
    # setup embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cuda"},  # Altere para "cuda" se tiver GPU
        encode_kwargs={"normalize_embeddings": True},
    )

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return db


def query_db(db, query_text):
    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # gather in a context
    context_text = "\n\n---\n\n".join(
        [f"{doc.page_content}" for doc, _score in results]
    )

    # return
    return context_text


if __name__ == "__main__":
    db = load_db()

    question = "Who Alice follow?"

    response = query_db(db, question)

    # prompt chat
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.",
            ),
            (
                "human",
                """Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}""",
            ),
        ]
    )

    # model creation
    llm = ChatQWEN()

    # pipeline
    chain = prompt | llm

    # ask
    print(
        chain.invoke(
            {
                "context": response,
                "question": question,
            }
        ).content
    )
