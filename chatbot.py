import streamlit as st
import google.generativeai as genai
# importing library
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
# st.image("image.png",use_column_width=True)

st.title("Beginner ChatBot")
st.sidebar.radio("Home",["Home page"])
but=st.sidebar.button("About home")
if but:
    st.write("""
- This app allows you to interact with an AI chatbot powered by Generative AI models.
- You can ask various types of questions, convert audio or image files into text, and even generate code.
- You can work with audio and video files. For example, you can convert an audio file to text or generate a transcript. You can also work with timestamps in the audio file for precise editing.
- You can extract text from images, making it easy to digitize printed content or handwritten notes.
- You can generate code from text in any programming language you want, whether it's Python, JavaScript, or C++.
- The chatbot is designed to assist you with educational inquiries, programming challenges, and general knowledge questions.
- With a user-friendly interface, you can easily navigate through different functionalities without any hassle.
- Explore the various options through the sidebar and unlock the full potential of this AI-powered tool!
""")


# st.header("Welcome to AI ChatBot")
genai.configure(api_key="AIzaSyB2c2dCl8a2DQQYAlm8sYeDnx5ItDSYjC8")
model=genai.GenerativeModel("gemini-1.5-flash-8b-exp-0924")
from IPython.display import Markdown
list=st.sidebar.selectbox("Select",["List of models","List of files"])
if "history" not in st.session_state:
    st.session_state.history=[]
if list=="List of models":
    but=st.sidebar.button("Show")
    if but:
        st.write(f"*{'Here is the list of all models'}*")
        for i in genai.list_models():
            st.write(f"**{i.name}**")
if list=="List of files":
    but=st.sidebar.button("Show")
    if but:
        st.write(f"*{'Here is the list of all files uploaded using this api'}*")
        for i in genai.list_files():
            st.write(f"**{i.name}**")
process=st.sidebar.radio("Choose",["Question answer","Image to Text","Audio to text","Text to code","Real Time Image To Text"])
if process=="Question answer":
    but=st.text_input("Enter prompt or question you want to ask then press enter")
    st.session_state.history.append(but)
    butt=st.button("Ask your question")
    if butt:
        response=model.generate_content(but)
        st.markdown(response.text)

    
if process=="Audio to text":
    file = st.file_uploader("Upload Your audio file")
    if file is not None:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        audio = genai.upload_file(file.name)
        input=st.text_input("Ask What you want to know about this audio")
        but=st.button("Ask your question")
        if but:
            st.session_state.history.append(input)
            response=model.generate_content((audio,input))
            st.markdown(response.text)
    else:
        st.warning("Please upload a valid audio file.")
if process=="Video to text":
    file = st.file_uploader("Upload Your audio file")
    if file is not None:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        video = genai.upload_file(file.name)
        input=st.text_input("Ask What you want to know about this Video")
        but=st.button("Ask your question")
        if but:
            st.session_state.history.append(input)
            response=model.generate_content((video,input))
            st.markdown(response.text)
    else:
        st.warning("Please upload a valid video file.")
if process=="Image to Text":
    file = st.file_uploader("Upload Your audio file")
    if file is not None:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        image = genai.upload_file(file.name)
        input=st.text_input("Ask What you want to know about this Image")
        but=st.button("Ask your question")
        if but:
            st.session_state.history.append(input)
            response=model.generate_content((image,input))
            st.markdown(response.text)
    else:
        st.warning("Please upload a valid image file.")
if process=="Text to code":
        input=st.text_input("You can ask your question in your desired programming language")
        but=st.button("Ask your question")
        if but:
            st.session_state.history.append(input)
            response=model.generate_content((input))
            st.markdown(response.text)
if process=="Real Time Image To Text":
    file = st.camera_input("You can use your camera to click pic and generate image about this")
    if file is not None:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        image = genai.upload_file(file.name)
        input=st.text_input("Ask What you want to know about this Image")
        but=st.button("Ask your question")
        if but:
            st.session_state.history.append(input)
            response=model.generate_content((image,input))
            st.markdown(response.text)
    else:
        st.warning("Please upload a valid image file.")
historyy=st.sidebar.button("Show history")
if historyy:
    st.subheader("Here is your history of the chat: ")
    for i in st.session_state.history:
        st.write(i)

st.balloons()
