# Hendrik Raubenheimer's Codex

## Design Choices

I opted for a RAG approach that uses PDFs as training data. The PDF format was chosen for its prevalence and common usage. \
I chose Gemini as my LLM of choice because of my familiarity with it. From experience I know its very easy to set up with conversation memory and has a generous free tier. In this project I was able to create a client that can facilitate conversations with memory in only 2 lines of code. \
I opted for Streamlit as my UI platform of choice. Streamlit has a reputation for being an easy and quick way of deploying a chatbot or dashboard. I can confirm I quickly came right with Streamlit as someone with no prior experience with it.

The training data consists of PDF documents. The first document is my CV, the second document is an old cover letter I chose for its additional information on my background and personality, and the third document is called 'Behaviour' and is custom made for this agent. 'Behaviour.pdf' is a direct attempt at giving the chatbot my personality and voice, while the first two documents are more focused towards providing information. It makes broad claims about how I communicate, and includes a list of phrases I frequently use. 

I explored the applicability of philosophy in this project. I have a deep-rooted passion for philosophy and can confidently say it has an influence on me. I speculatively included 3 philosophers I like in 'Behaviour' along with what philosophy of theirs I find inspiring.

This submission's bonus features include a drag and drop feature for additional training data, and a tone switcher that can switch between "Interview", "Storytelling", "Humble Brag" and "Trots Afrikaans (fun)".

## Sample Questions and Answers

**Question**: What kind of engineer are you? \
**Answer**: Right, so, if you're asking what kind of engineer I am, I'd put myself squarely in the realm of machine learning and artificial intelligence. My qualifications have given me a solid footing across computer science, data science, and of course, the mathematical side of things. Honestly, I live and breathe code, constantly looking for new ways to apply it, especially when it comes to solving real-world problems with data and AI.

**Question**: What are your strongest technical skills? \
**Answer**: Right, my strongest technical skills. I'd definitely highlight Java and Python as my core programming languages; I've got years of hands-on experience with both, using Java for more foundational work and Python being my go-to for anything related to data science and AI.
Beyond that, I'm very strong with SQL for database management and querying, and I'm quite proficient with Pandas for data manipulation within Python. When it comes to the AI side, I've got solid experience with TensorFlow for machine learning models, and I'm familiar with AWS for cloud deployments.
It's a blend of robust development skills and the specific tools that are essential for data and AI work.

**Question**: What are you most afraid of? \
**Answer**: Honestly, if I had to hit the nail on the head with that one, I'd say my greatest apprehension would be intellectual stagnation. In a field like Machine Learning and AI, things move at an incredible pace, and the thought of not being able to constantly live and learn, to keep pushing myself, or to see my skills become less relevant... that's a genuine concern.
I thrive on challenges, on diving deep into complex problems, and on building things that make a tangible difference. The idea of not being able to contribute meaningfully, or to feel like my passion isn't being applied to create a positive snowball effect in the real world – that's something I actively work against. I want to be where the problems are, where I can apply my grit and ambition, and ensure that fortune favours the bold in our pursuit of innovative solutions.

## Improvements to Be Made

The 'Behaviour.pdf' seems to have the desired effect on the chatbot, but my list of go-to phrases are generally overused. Additionally, there are certain phrases in the cover letter it also overuses. Its hard to definitively say what an influence the philosophy information has, but it seems to not have much influence. Occasionally the chatbot will refer to phrases like 'will to power', but there is not strong evidence that its speech is molded by the philosophy in anyway. I have also witnessed a fair bit of hallucination with regards to information about me. This could be improved with a lower temperature setting.

## Show Your Thinking

I primarily used GitHub copilot power by Claude Sonnet 4.

All drag and drop functionality for additional training data was made completely with AI. Almost everything else was generated with AI with my own modifications.

#### AI Prompt Timeline

*I started by getting copilot to make a RAG agent after I imported Gemini's API*

**Prompt:** Create a simple RAG agent built off Gemini's API, and that uses data in /Input \
**Response:**
```python
import os
import glob
import PyPDF2

# Load and concatenate text from all PDFs in ./Input
def load_pdfs(input_dir="./Input"):
    text = ""
    for pdf_file in glob.glob(os.path.join(input_dir, "*.pdf")):
        with open(pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    return text

# Minimal RAG: retrieve context and ask Gemini
def ask_gemini(query, context):
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = genai.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    context = load_pdfs()
    user_query = input("Ask a question: ")
    answer = ask_gemini(user_query, context)
    print("Gemini:", answer)
```

*For most optimal results I wanted to send through the PDF files themselves, not just their text*

**Prompt:** Instead of sending through the text of these pdfs to Gemini, send through the pdfs themselves \
**Response:**
```python
import os
import glob
import PyPDF2

# Load all PDF file paths from ./Input
def load_pdf_paths(input_dir="./Input"):
    return glob.glob(os.path.join(input_dir, "*.pdf"))

# Minimal RAG: send PDFs as files to Gemini (if supported)
def ask_gemini_with_files(query, pdf_paths):
    \# genai.generate_content supports file input via the 'files' parameter
    \# This assumes the API and SDK support file uploads
    files = []
    for path in pdf_paths:
        files.append({"file_path": path, "mime_type": "application/pdf"})
    prompt = f"Question: {query}\nPlease answer using the attached PDFs."
    response = genai.generate_content(prompt, files=files)
    return response.text

if __name__ == "__main__":
    pdf_paths = load_pdf_paths()
    user_query = input("Ask a question: ")
    answer = ask_gemini_with_files(user_query, pdf_paths)
    print("Gemini:", answer)
```

*At this point I realised my coding agent is not familiar with Gemini's API, so I decided to code manually for a bit given I have experience with the API. I began by checking how to convert pdf files to bytes*

**Prompt:** How can I read in a pdf in bytes \
**Response:**
In Python, you can read a PDF file in bytes by opening it with the "rb" (read-binary) mode:

```python
with open("path/to/file.pdf", "rb") as f:
    pdf_bytes = f.read()
```

This will load the entire PDF file into the variable pdf_bytes as a bytes object. You can then use this bytes object with libraries like PyPDF2, pdfplumber, or send it over a network, etc.

*I got a minimal RAG going, and asked copilot to convert it to a Streamlit app*

**Prompt:** Convert this to a Streamlit app \
**Response:**
```python
from google import genai
import os
import glob
import streamlit as st

def load_pdfs(input_dir="./Input"):
    data = []
    for pdf_file in glob.glob(os.path.join(input_dir, "*.pdf")):
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
            data.append(pdf_bytes)
    return data

st.title("PDF Content Summarizer")

if st.button("Analyze PDFs", type="primary"):
    with st.spinner("Processing PDFs..."):
        client = genai.Client()
        chat = client.chats.create(model="gemini-2.5-flash")
        pdf_data = load_pdfs()

        for pdf_bytes in pdf_data:
            chat.send_message(genai.types.Part.from_bytes(
                data=pdf_bytes,
                mime_type='application/pdf'
            ))
        response = chat.send_message("What is the content of these PDFs?")
        st.subheader("Gemini Response:")
        st.write(response.text)
```

*I noticed the PDFs would load in everytime I sent a message*

**Prompt:** Have the PDFs load in only once \
**Response:**
```python
if 'pdfs_loaded' not in st.session_state:
    with st.spinner("Loading PDFs..."):
        pdf_data = load_pdfs()
        
        for pdf_bytes in pdf_data:
            chat.send_message(genai.types.Part.from_bytes(
                data=pdf_bytes,
                mime_type='application/pdf'
            ))
        
        st.session_state.pdfs_loaded = True

if st.button("Analyze PDFs", type="primary"):
    with st.spinner("Analyzing..."):
        response = chat.send_message("What is the content of these PDFs?")
        st.subheader("Gemini Response:")
        st.write(response.text)
```

*Up till this point a hardcoded message would be sent through, but I required the user to be able to send through custom messages*

**Prompt:** Replace the button with a textpane that sends messages to Gemini, and write the responses \
**Response:***
```python
user_input = st.text_area("Ask Gemini about the PDFs:", key="user_input")

if st.button("Send", type="primary") and user_input.strip():
    with st.spinner("Gemini is thinking..."):
        response = chat.send_message(user_input)
        st.subheader("Gemini Response:")
        st.write(response.text)
```

*I noticed a bug that prevented the chatbot from remembering previous interactions. I figured it was an easy mistake to pick up and asked copilot to do it for me*

**Prompt:** Why can Gemini not retain memory on previous interactions \
**Response:**
```python
# Initialize chat session only once
if 'chat' not in st.session_state:
    # Initialize your model and chat here
    model = genai.GenerativeModel('gemini-2.5-pro')  # or whatever model you're using
    st.session_state.chat = model.start_chat()

# Use the persistent chat from session state
chat = st.session_state.chat
```

*I was now intent on adding a tone switcher. Still a bit unfamiliar with Streamlit, I asked copilot to write some skeleton code for a selectbox that I proceeded to customise*

**Prompt:** Add a selectbox that prints to console whenever an option is selected \ 
**Response:**
```python
# Optional selectbox for debugging/testing
st.sidebar.header("🔧 Debug Options")
debug_options = [
    "None",
    "Show Chat History",
    "Show Session State",
    "Show File List",
    "Test Connection",
    "Clear Memory"
]

selected_option = st.sidebar.selectbox(
    "Select Debug Action:",
    options=debug_options,
    index=0,
    help="Choose an option to execute debug actions"
)

# Handle selectbox selection and print to terminal
if selected_option != "None":
    print(f"[DEBUG] Selected option: {selected_option}")
    
    if selected_option == "Show Chat History":
        print(f"[DEBUG] Chat session state: {hasattr(st.session_state, 'chat')}")
    elif selected_option == "Show Session State":
        print(f"[DEBUG] Session state keys: {list(st.session_state.keys())}")
    elif selected_option == "Show File List":
        files = glob.glob("./Input/*")
        print(f"[DEBUG] Files in Input directory: {files}")
    elif selected_option == "Test Connection":
        print(f"[DEBUG] Testing Gemini connection...")
    elif selected_option == "Clear Memory":
        print(f"[DEBUG] Memory cleared (simulated)")
```

*I wanted to add functionality for the extension of the dataset with a drag and drop feature*

**Prompt:** Add a drag and drop feature to the app that allows the user to upload new PDFs for the chatbot to learn from \
**Response:**
```python
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
```
