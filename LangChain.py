import torch

# chat
from QWEN import ChatQWEN
from langchain_core.prompts import ChatPromptTemplate

# db related
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def load_db(CHROMA_PATH="chromadb/", MODEL_NAME="Alibaba-NLP/gte-multilingual-base"):
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # setup embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": device,
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


def load_chain():
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

    return chain


def query(question, db, chain):
    context, sources = query_db(db, question)

    print(f"Context:\n{context}\n*************************")

    # ask
    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    ).content
    print(f"Answer:\n{answer}\n*************************")

    print(f"Sources:\n{sources}")

    return answer, sources


if __name__ == "__main__":
    db = load_db()

    question = "Cor do cabelo de Van Helsing"

    context, sources = query_db(db, question)

    # model creation
    chain = load_chain()

    print(f"Context:\n{context}\n*************************")

    # ask
    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    ).content
    print(f"Answer:\n{answer}\n*************************")

    print(f"Sources:\n{sources}")
