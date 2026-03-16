import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# 1. Setup Groq (The Brain) and HuggingFace (The Translator)
# We use llama-3.3-70b-versatile as it is the stable flagship model.
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# This model runs locally on your Mac for free
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def get_pinecone_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX", "documind")

    if index_name not in [idx.name for idx in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=384, # Dimensions for bge-small
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

def ingest_document(file_path: str, tenant_id: str):
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    vector_store = PineconeVectorStore(pinecone_index=get_pinecone_index(), namespace=tenant_id)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    return f"Successfully processed {len(documents)} pages."

def query_documents(question: str, tenant_id: str):
    vector_store = PineconeVectorStore(pinecone_index=get_pinecone_index(), namespace=tenant_id)
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response)