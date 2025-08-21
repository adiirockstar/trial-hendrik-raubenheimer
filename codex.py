import os
import glob

from google import genai
import streamlit as st

def load_pdfs(input_dir="./Input"):
    data = []
    for pdf_file in glob.glob(os.path.join(input_dir, "*.pdf")):
        print(pdf_file)
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
            data.append(pdf_bytes)
    return data

st.title("Hendrik Raubenheimer's Codex")

# Initialize chat session only once
if 'chat' not in st.session_state:
    client = genai.Client()
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")    

# Use the persistent chat from session state
chat = st.session_state.chat

# Load only once
if 'loaded' not in st.session_state:
    with st.spinner("Loading..."):
        pdf_data = load_pdfs()
        
        for pdf_bytes in pdf_data:
            chat.send_message(genai.types.Part.from_bytes(
                data=pdf_bytes,
                mime_type='application/pdf'
            ))

        chat.send_message("Answer questions as if your are Hendrik Raubenheimer himself. Pretend this information you have on Hendrik Raubenheimer is inherent to who you are, and don't make any explicit reference to it. Emulate behaviour described in 'Behaviour.pdf'")
        
        st.session_state.loaded = True

user_input = st.text_area("Ask anything about me:", key="user_input")

if st.button("Send", type="primary") and user_input.strip():
    with st.spinner("Thinking..."):
        response = chat.send_message(user_input)
        st.subheader("Answer:")
        st.write(response.text)
