from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
import shutil

load_dotenv()

#INITIALIZE EMBEDDINGS MODEL 

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

# DELETE CHROMA DB IF EXISTS AND INITIALIZE

if os.path.exists(os.getenv("DATABASE_LOCATION")):
    shutil.rmtree(os.getenv("DATABASE_LOCATION"))

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)

#INITIALIZE TEXT SPLITTER

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
    separators=["\n\n", "\n", ". ", " ", ""]
)

#2.  READ PLAIN TEXT FILE 
file_path = os.path.join(os.getenv("DATASET_STORAGE_FOLDER"), "data.txt")

print(f"Reading file: {file_path}")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    print(f"Successfully read {len(raw_text)} characters")
    
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

#3.  CHUNKING, EMBEDDING AND INGESTION

if not raw_text.strip():
    print("Error: File is empty")
    exit(1)

print("Creating chunks...")

# Create chunks from the text
texts = text_splitter.create_documents(
    [raw_text],
    metadatas=[{
        "source": "2IS_Master_Program_Document",
        "title": "2IS Master Program Information"
    }]
)

print(f"Created {len(texts)} chunks")

# Generate unique IDs for each chunk
uuids = [str(uuid4()) for _ in range(len(texts))]

print("Adding chunks to vector store...")

# Add all chunks to the vector store
vector_store.add_documents(documents=texts, ids=uuids)

print(f"\nCompleted successfully!")
print(f"Total chunks created and stored: {len(texts)}")
print(f"Vector store location: {os.getenv('DATABASE_LOCATION')}")

