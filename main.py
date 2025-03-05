# Title: main.py
# 2025/3/2 13:51
import io
import hashlib
import streamlit as st
from openai import AuthenticationError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import get_chat_response, process_file
from langchain.memory import ConversationBufferMemory


def compute_file_hash(file):
    file.seek(0)
    content = file.read()
    file.seek(0)  # 重置指针以便后续操作
    return hashlib.md5(content).hexdigest()


def create_null_file():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "null")
    c.save()
    buffer.seek(0)
    st.session_state["pdf_file"] = buffer
    st.session_state["pdf_filename"] = None


st.title("🤖私人定制GPT")
with st.sidebar:
    api_key = st.text_input("🔑请输入DashScope API密钥：", type="password")  # 输入框，类型为密码输入
    st.markdown("[🔍获取DashScope API密钥](https://www.aliyun.com/product/bailian)")
    st.session_state["file_tag"] = st.checkbox("是否上传外部文件？")
    if st.session_state["file_tag"]:
        uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
        if uploaded_file:
            st.session_state["pdf_file"] = uploaded_file
            st.session_state["pdf_filename"] = uploaded_file.name
        else:
            create_null_file()
    else:
        create_null_file()

if st.button("开启新聊天"):
    # 仅重置对话相关状态，保留文件缓存
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
    st.session_state["messages"] = [{"role": "ai", "content": "我是一个无所不能的AI，找我什么事？？"}]

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
    st.session_state["messages"] = [{"role": "ai", "content": "我是一个无所不能的AI，找我什么事？？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if st.session_state["file_tag"] and st.session_state["pdf_filename"] is None:
        st.info("请上传您的外部文件")
        st.stop()

    current_file = st.session_state["pdf_file"]
    current_hash = compute_file_hash(current_file)

    # 检查文件是否变化
    if "cached_file_hash" not in st.session_state or st.session_state["cached_file_hash"] != current_hash:
        try:
            with st.spinner("正在处理文件..."):
                retriever = process_file(current_file, api_key)
                st.session_state["cached_retriever"] = retriever
                st.session_state["cached_file_hash"] = current_hash
        except ValueError as e:
            # 捕获 ValueError 并提示用户
            st.error("❌ 请输入正确的DashScope API Key")
            st.stop()
        except Exception as e:
            # 捕获其他异常并提示用户
            st.error(f"❌ 发生错误：{str(e)}")
            st.stop()
    else:
        retriever = st.session_state["cached_retriever"]

    # 调用对话函数
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中..."):
        response = get_chat_response(
            prompt,
            st.session_state["memory"],
            retriever,
            api_key
        )
        st.session_state["messages"].append({"role": "ai", "content": response["answer"]})
        st.chat_message("ai").write(response["answer"])
