download Ollama : 
https://ollama.com/
download large model: 
paste in cmd :
ollama pull phi3:mini
download embedding model
paste in cmd:
ollama pull mxbai-embed-large

navigate to the code folder (Local-RAG-with-Ollama)
create venv and download requirement.txt
in the terminal :
python -m venv venv
activating the env :
in the terminal :
venv/Scripts/Activate or source venv/Scripts/Activate on mac
installing all libraries:
pip install -r requierements.txt



create .env file
inside the file :

EMBEDDING_MODEL = "mxbai-embed-large:latest"
CHAT_MODEL = "phi3:mini"
MODEL_PROVIDER = "ollama"
DATASET_STORAGE_FOLDER = "datasets/"
SNAPSHOT_STORAGE_FILE = "snapshot.txt"
DATABASE_LOCATION = "chroma_db"
COLLECTION_NAME = "rag_data"



victorising the data :
python 2_chunking_embedding_ingestion.py

running the chatbot:
streamlit run 3_chatbot.py

