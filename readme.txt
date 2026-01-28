python version : Python 3.10.0 

download Ollama :  https://ollama.com/

download large model: 
 in cmd :
ollama pull phi3:mini

download embedding model
in cmd:
ollama pull mxbai-embed-large

navigate to the code folder (Local-RAG-with-Ollama)
create venv , activate it and download requirement.txt
in the terminal :

python -m venv venv     to create ur venv

venv/Scripts/Activate   to activate ur venv
or source venv/Scripts/Activate on mac


installing all libraries:
pip install -r requierements.txt 
(in case of error "no requirements.txt found " replace it with the full path for requierements.txt)


victorising the data :
python 2_chunking_embedding_ingestion.py        to victorise your data using chroma_db


run the chatbot:
streamlit run 3_chatbot.py

