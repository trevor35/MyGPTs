# Title:
# 2025/3/2 13:51
import streamlit as st
from utils import get_chat_response
from langchain.memory import ConversationBufferMemory

st.title("🤖私人定制GPT")
with st.sidebar:
    api_key = st.text_input("🔑请输入DashScope API密钥：", type="password")
    st.markdown("[🔍获取DashScope API密钥](https://www.aliyun.com/product/bailian)")

cl = st.button("开启新聊天")
if cl:
    st.session_state.clear()

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "我是一个无所不能的AI，找我什么事？？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])



prompt = st.chat_input()
if prompt:
    if not api_key:
        st.info("请输入您的DashScope API密钥")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍后。。"):
        response = get_chat_response(prompt, st.session_state["memory"], api_key)
        st.session_state["messages"].append({"role": "ai", "content": response})
        st.chat_message("ai").write(response)