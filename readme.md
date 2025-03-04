```markdown
# 🤖 私人定制GPT - 智能聊天助手

一个基于Streamlit和阿里云千问模型的个性化对话应用，具备对话记忆功能，赋予AI独特的"暴躁"人设。

---

## 🌟 核心功能

- **个性化AI角色**  
  预设脾气暴躁、阴阳怪气的人设，提供趣味交互体验
- **持续对话记忆**  
  采用`ConversationBufferMemory`实现多轮对话上下文跟踪
- **安全密钥管理**  
  侧边栏密码输入保护API密钥安全
- **即时会话管理**  
  一键清空对话历史，随时开始新话题
- **实时流式响应**  
  内置加载状态提示，提升交互体验

---

## 🛠️ 技术栈

| 类别         | 技术/工具                                                                 |
|--------------|--------------------------------------------------------------------------|
| **前端框架** | Streamlit `1.32.0+`                                                     |
| **AI框架**   | LangChain `0.1.12+`                                                     |
| **对话模型** | 阿里云千问Turbo (`qwen-turbo-2024-02-06`)                                |
| **核心组件** | `ConversationChain`, `ChatPromptTemplate`, `ConversationBufferMemory`    |

---
```

---

### 运行应用
```bash
pip install -r requirement.txt --timeout 1000
conda activate GPT
streamlit run main.py
```

---

## ⚙️ 配置说明

1. **获取API密钥**  
   前往[阿里云百炼平台](https://www.aliyun.com/product/bailian)申请DashScope API密钥

2. **密钥使用**  
   运行后在侧边栏输入密钥，自动应用于所有对话

---

## 📂 项目结构
```
.
├── main.py                 # 主应用文件
├── utils.py               # AI响应生成模块
└── requirements.txt       # 依赖列表（建议包含）
```

---

## 📌 注意事项

⚠️ 密钥安全  
❗ 本地运行时密钥仅存于内存，刷新页面需重新输入  
🔄 模型服务  
⏳ 使用阿里云DashScope的兼容模式API端点

---

## 📜 开源协议
MIT License © 2025 [Your Name]
```