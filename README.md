# Hendrik Raubenheimer's Codex

## Design Choices

I opted for a RAG approach that uses PDFs as training data. The PDF format was chosen for its prevalence and common usage. \
I chose Gemini as my LLM of choice because of my familiarity with it. From experience I know its very easy to set up with conversation memory and has a generous free tier. In this project I was able to create a client that can facilitate conversations with memory in only 2 lines of code. \
I opted for Streamlit as my UI platform of choice. Streamlit has a reputation for being an easy and quick way of deploying a chatbot or dashboard. I can confirm I quickly came right with Streamlit as someone with no prior experience with it.

The training data consists of PDF documents. The first document is my CV, the second document is an old cover letter I chose for its additional information on my background and personality, and the third document is called 'Behaviour' and is custom made for this agent. 'Behaviour.pdf' is a direct attempt at giving the chatbot my personality and voice, while the first two documents are more focused towards providing information. It makes broad claims about how I communicate, and includes a list of phrases I frequently use. 

I explored the applicability of philosophy in this project. I have a deep-rooted passion for philosophy and can confidently say it has an influence on me. I speculatively included 3 philosophers I like in 'Behaviour' along with what philosophy of theirs I like.

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

The 'Behaviour.pdf' seems to have the desired effect on the chatbot, but my list of go-to phrases are generally overused. Additionally, there are certain phrases in the cover letter it also overuses. Its hard to definitively say what an influence the philosophy information has, but it seems to not have much influence. Occasionally the chatbot will refer to phrases like 'will to power', but there is not strong evidence that its speech is molded by the philosophy in anyway.

## Show Your Thinking

I primarily used GitHub copilot power by Claude Sonnet 4.

#### AI Prompt Timeline

**Prompt:** Create a simple RAG agent built off Gemini's API, and that uses data in /Input (With 'from google import genai' already typed out) \
**Response:** \
<code>import os
import glob
import PyPDF2

\# Load and concatenate text from all PDFs in ./Input
def load_pdfs(input_dir="./Input"):
    text = ""
    for pdf_file in glob.glob(os.path.join(input_dir, "*.pdf")):
        with open(pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    return text

\# Minimal RAG: retrieve context and ask Gemini
def ask_gemini(query, context):
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = genai.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    context = load_pdfs()
    user_query = input("Ask a question: ")
    answer = ask_gemini(user_query, context)
    print("Gemini:", answer)</code>
