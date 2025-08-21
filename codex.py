import os
import glob

from google import genai
import streamlit as st

# Load in the pdf files as bytes
def load_pdfs(input_dir="./Input"):
    data = []
    for pdf_file in glob.glob(os.path.join(input_dir, "*.pdf")):
        print(pdf_file)
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
            data.append(pdf_bytes)
    return data

# Save uploaded files to the Input directory
def save_uploaded_files(uploaded_files, input_dir="./Input"):
    """Save uploaded files to the Input directory"""
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(input_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(file_path)
    return saved_files

# Process newly uploaded files and add them to the chat
def process_new_files(chat, new_files):
    """Process newly uploaded files and add them to the chat"""
    for file_path in new_files:
        if file_path.lower().endswith('.pdf'):
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
                chat.send_message(genai.types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type='application/pdf'
                ))

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

# File upload section
st.sidebar.header("📁 Upload Files")
uploaded_files = st.sidebar.file_uploader(
    "Drag and drop files here or click to browse",
    accept_multiple_files=True,
    type=['pdf', 'txt', 'doc', 'docx'],
    help="Upload files to add to Hendrik's knowledge base"
)

# If files are uploaded, process them
if uploaded_files:
    with st.sidebar:
        if st.button("Add Files to Knowledge Base", type="primary"):
            with st.spinner("Processing uploaded files..."):
                try:
                    saved_files = save_uploaded_files(uploaded_files)
                    process_new_files(chat, saved_files)
                    
                    st.success(f"Successfully added {len(saved_files)} file(s):")
                    for file_path in saved_files:
                        st.write(f"• {os.path.basename(file_path)}")
                    
                    # Clear the uploaded files from session
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")

# Display current files in Input directory
with st.sidebar.expander("📋 Current Files", expanded=False):
    input_files = glob.glob("./Input/*")
    if input_files:
        for file_path in input_files:
            st.write(f"• {os.path.basename(file_path)}")
    else:
        st.write("No files in Input directory")

# Optional selectbox for switching tone
st.sidebar.header("🔧 Tone Switcher")
debug_options = [
    "None",
    "Interview",
    "Storytelling",
    "Humble Brag",
    "Trots Afrikaans (fun)"
]

selected_option = st.sidebar.selectbox(
    "Select Tone:",
    options=debug_options,
    index=0,
    help="Choose an option to change tone"
)

# Handle selectbox selection and print to terminal
if selected_option != "None":

    if selected_option == "Interview":
        chat.send_message("You are now in interview mode. Answer questions in a formal and professional manner. Do so until instructed to change tone mode.")
    elif selected_option == "Storytelling":
        chat.send_message("You are now in storytelling mode. Answer questions with a narrative style and using anecdotes. Do so until instructed to change tone mode.")
    elif selected_option == "Humble Brag":
        chat.send_message("You are now in humble brag mode. Be more boastful and self-promoting. Do so until instructed to change tone mode.")
    elif selected_option == "Trots Afrikaans (fun)":
        chat.send_message("You are now in Trots Afrikaans mode. Use as much Afrikaans and South African slang as you can. Do so until instructed to change tone mode.")

user_input = st.text_area("Ask anything about me:", key="user_input")

# Send the user's input to the chat
if st.button("Send", type="primary") and user_input.strip():
    with st.spinner("Thinking..."):
        response = chat.send_message(user_input)
        st.subheader("Answer:")
        st.write(response.text)
