import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
import os

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Configuração do modelo ChatGPT
openai_api_key = "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"
model_chatgpt = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")

# Função para carregar dados
def load_txt_data():
    loader = TextLoader(file_path="knowledge_base.txt")  # Substitua pelo caminho correto
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    documents = loader.load()
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

retriever = load_txt_data()

# Configuração do prompt e do modelo
rag_template = """
Você é um atendente de uma instituição financeira. Seu trabalho é conversar com os clientes, consultando a base de
conhecimentos da empresa, e dar uma resposta simples e precisa para ele, baseada na base de dados fornecida como
contexto.

Contexto: {context}

Pergunta do cliente: {question}
"""
prompt = ChatPromptTemplate.from_template(rag_template)

# Função para interagir com o modelo
def chat(user_input):
    if not user_input:
        return "Por favor, digite uma pergunta."
    
    context = retriever.get_relevant_documents(user_input)
    formatted_input = prompt.format_prompt(context=context, question=user_input)
    response = model_chatgpt(formatted_input.to_messages())
    return response.content

# Interface com Streamlit
st.title("Oráculo Financeiro 💬")
st.write("Bem-vindo ao assistente virtual da instituição financeira. Pergunte algo!")

# Caixa de entrada do usuário
user_input = st.text_input("Digite sua pergunta:")

# Botão para enviar a pergunta
if st.button("Enviar"):
    resposta = chat(user_input)
    st.write(f"**Assistente:** {resposta}")