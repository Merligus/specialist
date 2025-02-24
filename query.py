# chat
from QWEN import ChatQWEN
from langchain_core.prompts import ChatPromptTemplate

# db related
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chromadb/"

# free model
MODEL_NAME = "Alibaba-NLP/gte-multilingual-base"


def load_db():
    # setup embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cuda",
            "trust_remote_code": True,
        },
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
    sources = "\n".join([doc.metadata["source"] for doc, _score in results])

    # return
    return context_text, sources


if __name__ == "__main__":
    db = load_db()

    question = "Cor do cabelo de Van Helsing"

    context, sources = query_db(db, question)

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

Answer the question based on the above context in question's original language: {question}""",
            ),
        ]
    )

    # model creation
    llm = ChatQWEN()

    # pipeline
    chain = prompt | llm

    print(f"Context:\n{context}\n")

    # ask
    print(
        chain.invoke(
            {
                "context": context,
                "question": question,
            }
        ).content
    )

    print(f"\nSources:\n{sources}")
