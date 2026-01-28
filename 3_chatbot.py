# import basics
import os
from dotenv import load_dotenv

# import streamlit
import streamlit as st

# import langchain
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate

# load environment variables
load_dotenv()  

#INITIALIZE EMBEDDINGS MODEL  

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

#INITIALIZE CHROMA VECTOR STORE  

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)

# INITIALIZE CHAT MODEL 

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0  # Keep at 0 for factual responses
)

# CREATE RETRIEVER

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
)

#CREATE CUSTOM PROMPT

prompt_template = """You are a helpful assistant for the 2IS Master program at University of Toulouse Capitole.

Use the following pieces of context to answer the question at the end. 

CRITICAL INSTRUCTIONS:
1. ONLY answer based on the provided context below
2. If the context doesn't contain the answer, say "I don't have this information in my database"
3. NEVER make up or guess information
4. Quote specific details from the context when possible
5. Be concise and direct in your answers

Context:
{context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

#CREATE QA CHAIN

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" means put all context into one prompt
    retriever=retriever,
    return_source_documents=True,  # Return the source chunks used
    chain_type_kwargs={"prompt": PROMPT}
)

# STREAMLIT APP  

# initiating streamlit app

st.set_page_config(page_title="RAG Chatbot")
st.title("RAG Chatbot - 2IS Master Program")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# create the input bar
user_question = st.chat_input("Ask me anything about the 2IS Master program...")

# did the user submit a prompt?
if user_question:
    # add the user message to chat history and display
    st.session_state.messages.append(HumanMessage(user_question))
    
    with st.chat_message("user"):
        st.markdown(user_question)

    # show a spinner while processing
    with st.spinner("Searching documents..."):
        # invoke the QA chain
        result = qa_chain.invoke({"query": user_question})
        
        ai_message = result["result"]
        source_docs = result.get("source_documents", [])

    # display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(ai_message)
        
        # Optional: Show source documents in an expander
        if source_docs:
            with st.expander("📚 View Source Documents"):
                for i, doc in enumerate(source_docs, 1):
                    st.markdown(f"**Source {i}:**")
                    st.text(doc.page_content[:200] + "...")
                    st.markdown("---")
    
    # add assistant message to chat history
    st.session_state.messages.append(AIMessage(ai_message))
