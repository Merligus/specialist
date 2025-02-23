from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import shutil

CHROMA_PATH = "chromadb/"

INPUT_PATH = "./data/books/alice_segmented/"

# free models
# MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # english (small and fast)
# MODEL_NAME = ("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")  # multiple languages
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"  # english (best quality)

# setup embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)

# load documents
raw_documents = DirectoryLoader(INPUT_PATH, glob="*.txt").load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100, length_function=len, add_start_index=True
)
documents = text_splitter.split_documents(raw_documents)
print(f"Split {len(raw_documents)} documents into {len(documents)} chunks.")

# Clear out the database first.
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)

# Create a new DB from the documents.
db = Chroma.from_documents(
    documents,
    embeddings,
    persist_directory=CHROMA_PATH,
    collection_metadata={"hnsw:space": "cosine"},
)
print(f"Saved {len(documents)} chunks to {CHROMA_PATH}.")
