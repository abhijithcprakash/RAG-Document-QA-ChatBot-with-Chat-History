# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.runnables.history import RunnableWithMessageHistory

# import chromadb

# import os
# from io import BytesIO
# from dotenv import load_dotenv
# load_dotenv()
# os.environ["HUGGINGFACE_API"] = os.getenv('HUGGINGFACE_API')

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# st.title("Conversational RAG with PDF uploads and Chat History")
# st.write("Upload PDF's and chat with their content")

# api_key = st.text_input("Enter your Groq API key: ", type="password")


# if api_key:
#     llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")

#     # Chat interface
#     session_id = st.text_input("Session ID", value='default_session')

#     # Statefully manage chat history
#     if 'store' not in st.session_state:
#         st.session_state.store = {}

#     uploaded_files=st.file_uploader("Choose A PDf file",type="pdf",accept_multiple_files=True)
#     ## Process uploaded  PDF's
#     if uploaded_files:
#         documents=[]
#         for uploaded_file in uploaded_files:
#             temppdf=f"./temp.pdf"
#             with open(temppdf,"wb") as file:
#                 file.write(uploaded_file.getvalue())
#                 file_name=uploaded_file.name

#             loader=PyPDFLoader(temppdf)
#             docs=loader.load()
#             documents.extend(docs)


#         # Split and create embeddingd for the documents
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
#         splits = text_splitter.split_documents(documents)

#         chromadb.api.client.SharedSystemClient.clear_system_cache()

#         vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
#         retriever = vectorstore.as_retriever()

#         contextualize_q_system_prompt = (
#             "Given a chat history and the latest user question"
#             "which might reference context in the chat history, "
#             "formulate a standalone question which can be understood "
#             "without the chat history. DO NOT answer the question, "
#             "just reformulate it if needed and otherwise return it as is."
#         )

#         contextualize_q_prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", contextualize_q_system_prompt),
#                 MessagesPlaceholder("chat_history"),
#                 ("human", "{input}"),
#             ]
#         )

#         history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

#         # Answer question
#         system_prompt = (
#             "You are an assistant for question-answering tasks. "
#             "Use the following pieces of retrieved context to answer "
#             "the question. If you don't know the answer, say that you "
#             "don't know. Use three sentences mmaximum and keep the "
#             "answer concise."
#             "\n\n"
#             "{context}"
#         )

#         qa_prompt = ChatPromptTemplate.from_messages(
#             [
#                 ("system", system_prompt),
#                 MessagesPlaceholder("chat_history"),
#                 ("human", "{input}"),
#             ]
#         )

#         question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
#         rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

#         def get_session_history(session_id:str)->BaseChatMessageHistory:
#             if session_id not in st.session_state.store:
#                 st.session_state.store[session_id] = ChatMessageHistory()
#             return st.session_state.store[session_id]
        
#         conversational_rag_chain = RunnableWithMessageHistory(
#             rag_chain,get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )


#         user_input = st.text_input("Your Question")
#         if user_input:
#             session_history = get_session_history(session_id)
#             response = conversational_rag_chain.invoke(
#                 {"input":user_input},
#                 config={
#                     "configurable": {"session_id":session_id}
#                 },
#             )
#             st.write(st.session_state.store)
#             st.write("Assistant: ", response["answer"])
#             st.write("Chat History", session_history.messages)
# else:
#     st.warning("Please enter the GROQ API key")


import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables.history import RunnableWithMessageHistory

import chromadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["HUGGINGFACE_API"] = os.getenv('HUGGINGFACE_API')

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Streamlit page settings
st.set_page_config(page_title="Conversational RAG 🤖📚", layout="wide")
st.title("📚 Conversational RAG with PDF Uploads and Chat History")
st.caption("Upload PDF files, chat with them intelligently, and maintain your session history!")

# Sidebar for API and session settings
with st.sidebar:
    st.header("🔐 Settings")
    api_key = st.text_input("Enter your Groq API key", type="password", placeholder="Your-Groq-API-Key")
    session_id = st.text_input("Session ID", value="default_session", help="Unique ID to maintain chat history.")

# Main app
if api_key:
    llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")

    # Initialize session storage
    if 'store' not in st.session_state:
        st.session_state.store = {}

    # Upload section
    st.subheader("📄 Upload your PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        documents = []
        with st.spinner("Processing documents... 📄✨"):
            for uploaded_file in uploaded_files:
                temp_path = "./temp.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                loader = PyPDFLoader(temp_path)
                docs = loader.load()
                documents.extend(docs)

            # Split documents and create vectorstore
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
            splits = text_splitter.split_documents(documents)

            chromadb.api.client.SharedSystemClient.clear_system_cache()
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
            retriever = vectorstore.as_retriever()

            # Create history-aware retriever
            contextualize_q_system_prompt = (
                "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question. DO NOT answer the question."
            )
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

            # Create QA chain
            system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the retrieved context to answer the question. "
                "If unknown, say so. Keep answers concise (max 3 sentences)."
                "\n\n{context}"
            )
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

            # Session-based history
            def get_session_history(session_id: str) -> BaseChatMessageHistory:
                if session_id not in st.session_state.store:
                    st.session_state.store[session_id] = ChatMessageHistory()
                return st.session_state.store[session_id]

            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

        st.success("Documents processed successfully! You can now chat. 🚀")

        # Chat section
        st.subheader("💬 Ask Questions")
        user_input = st.text_input("Type your question here...")

        if user_input:
            with st.spinner("Thinking... 💭"):
                session_history = get_session_history(session_id)
                response = conversational_rag_chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}},
                )
                st.chat_message("assistant").markdown(response["answer"])

        # Tabs for chat history and debug
        tabs = st.tabs(["🕑 Chat History", "🛠 Debug Info"])

        with tabs[0]:
            st.info("Below is your conversation history for this session:")
            session_history = get_session_history(session_id)
            for msg in session_history.messages:
                if msg.type == "human":
                    st.chat_message("user").markdown(msg.content)
                else:
                    st.chat_message("assistant").markdown(msg.content)

        with tabs[1]:
            st.caption("Session State Debugging")
            st.json(st.session_state.store)

    else:
        st.info("Please upload one or more PDFs to start the conversation.")

else:
    st.warning("🚨 Please enter your Groq API key in the sidebar to continue.")
