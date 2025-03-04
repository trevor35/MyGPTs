## Title: utils.py
# 2025/3/2 13:51

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_file(upload_file, api_key):
    # 读取文件内容并重置指针
    file_content = upload_file.read()
    upload_file.seek(0)

    # 写入临时文件
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as f:
        f.write(file_content)

    # 加载并分割PDF
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", "。", "，", ",", "、", ""]
    )
    texts = text_splitter.split_documents(docs)

    # 生成嵌入并创建向量库
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v2",
        dashscope_api_key=api_key
    )
    db = FAISS.from_documents(texts, embeddings)
    return db.as_retriever()


def get_chat_response(question, memory, retriever, api_key):
    model = ChatOpenAI(
        model="qwen-turbo-2024-02-06",
        openai_api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    return qa.invoke({"chat_history": memory, "question": question})