import streamlit as st
import google.generativeai as genai
import time

# ================= App Config =================
st.set_page_config(page_title="Kunal Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: "Segoe UI", sans-serif;
    }
    .chat-bubble-user {
        background-color: #1f77b4;
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        width: fit-content;
        max-width: 80%;
        align-self: flex-end;
    }
    .chat-bubble-bot {
        background-color: #2e2e2e;
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        width: fit-content;
        max-width: 80%;
        align-self: flex-start;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: bold;
        color: #00c8ff;
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #00c8ff;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0099cc;
    }
    </style>
""", unsafe_allow_html=True)

# ================= Title =================
st.markdown("<h1 style='text-align: center; color: #00c8ff;'>🤖 Kunal's AI ChatBot</h1>", unsafe_allow_html=True)
st.write("---")

# ================= Sidebar =================
st.sidebar.markdown("<p class='sidebar-title'>📌 Menu</p>", unsafe_allow_html=True)

if st.sidebar.button("ℹ️ About App"):
    st.sidebar.success("""
    - AI-powered chatbot with Generative AI.  
    - Supports Q&A, Image-to-Text, Audio-to-Text, and Code Generation.  
    - Upload media or ask coding/educational queries.  
    """)

# ================= API Setup =================
genai.configure(api_key="AIzaSyBFkxiJKOthmr75wJT6KGchWDJcf9j3GP4")  # replace with your key
model = genai.GenerativeModel("gemini-2.5-flash")

# ================= Session State =================
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar options
list_option = st.sidebar.selectbox("🔍 Explore", ["None", "List of models", "List of files"])
if list_option == "List of models" and st.sidebar.button("Show Models"):
    st.info("**Available Models:**")
    for i in genai.list_models():
        st.code(i.name, language="yaml")

if list_option == "List of files" and st.sidebar.button("Show Files"):
    st.info("**Uploaded Files:**")
    for i in genai.list_files():
        st.code(i.name, language="yaml")

# ================= Process Options =================
process = st.sidebar.radio("⚡ Choose Action", 
                           ["Question Answer", "Text to Code", "Image to Text", "Audio to Text", "Real-Time Image"])

# ================= Q&A Mode =================
if process == "Question Answer":
    prompt = st.text_input("💡 Ask me anything:")
    if st.button("🚀 Send") and prompt:
        st.session_state.history.append(("user", prompt))
        with st.spinner("🤖 Thinking..."):
            response = model.generate_content(prompt)
            time.sleep(1)
        st.session_state.history.append(("bot", response.text))

# ================= Text to Code =================
if process == "Text to Code":
    prompt = st.text_area("💻 Enter your coding request:")
    if st.button("🛠️ Generate Code") and prompt:
        st.session_state.history.append(("user", prompt))
        with st.spinner("⚙️ Generating Code..."):
            response = model.generate_content(prompt)
            time.sleep(1)
        st.session_state.history.append(("bot", response.text))

# ================= Audio to Text =================
if process == "Audio to Text":
    file = st.file_uploader("🎤 Upload your audio file", type=["mp3", "wav"])
    if file:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        audio = genai.upload_file(file.name)
        prompt = st.text_input("Ask about this audio:")
        if st.button("🎧 Process Audio") and prompt:
            st.session_state.history.append(("user", prompt))
            with st.spinner("🔊 Analyzing Audio..."):
                response = model.generate_content([audio, prompt])
            st.session_state.history.append(("bot", response.text))

# ================= Image to Text =================
if process == "Image to Text":
    file = st.file_uploader("🖼️ Upload an image", type=["jpg", "png"])
    if file:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        image = genai.upload_file(file.name)
        prompt = st.text_input("Ask about this image:")
        if st.button("📷 Process Image") and prompt:
            st.session_state.history.append(("user", prompt))
            with st.spinner("🖼️ Analyzing Image..."):
                response = model.generate_content([image, prompt])
            st.session_state.history.append(("bot", response.text))

# ================= Real-Time Image =================
if process == "Real-Time Image":
    file = st.camera_input("📸 Capture an image")
    if file:
        with open("captured_image.png", "wb") as f:
            f.write(file.getbuffer())
        image = genai.upload_file("captured_image.png")
        prompt = st.text_input("Ask about this captured image:")
        if st.button("🔍 Analyze Captured Image") and prompt:
            st.session_state.history.append(("user", prompt))
            with st.spinner("📸 Processing Image..."):
                response = model.generate_content([image, prompt])
            st.session_state.history.append(("bot", response.text))

# ================= Chat History =================
st.write("## 💬 Conversation")
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'>🙋 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {msg}</div>", unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.sidebar.success("Chat history cleared!")

# 🎉 Fun animation
# st.balloons()
