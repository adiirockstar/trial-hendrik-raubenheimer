# Hendrik Raubenheimer – Trial Project Assessment

**Repository:** [https://github.com/henryraubenheimer/codex](https://github.com/henryraubenheimer/codex)

## Rubric Evaluation

| Category | Score (0–5) | Notes |
| --- | --- | --- |
| Context Handling | 3 | Loads PDF bytes directly into the conversation without selective retrieval, which risks context dilution and hallucinations. |
| Agentic Thinking | 3 | Includes a tone switcher and persona priming, but modes are shallow and contain a bug. |
| Use of Personal Data | 3 | Incorporates CV, cover letter, and a custom “Behaviour” document, though dataset is small and unstructured. |
| Build Quality | 2 | Streamlit app runs but lacks tests, error handling, and setup guidance; tone switcher bug undermines feature. |
| Voice & Reflection | 3 | README reflects on design choices and sample responses in the candidate’s voice. |
| Bonus Effort | 3 | Drag‑and‑drop uploads and tone switcher show creative polish. |
| AI Build Artifacts | 3 | README documents prompt timeline and AI assistance. |
| RAG Usage (Optional) | 2 | Claims RAG but simply uploads entire PDFs; no chunking or retrieval mechanism. |
| Submission Completeness | 4 | Provides repository, deployment link, and demo video reference; minor documentation gaps remain. |

**Total Score: 26 / 45**

## Critical Feedback & Suggestions

### 1. Entire PDFs injected without retrieval
`load_pdfs` and the initial load loop send whole files as bytes to the chat without any retrieval layer, leading to scalability and relevance issues
`codex.py` lines 55–63.

*Suggestions*
- Chunk PDF text and index with embeddings (e.g., FAISS or `langchain`).
- Retrieve top‑k relevant chunks per query instead of sending all bytes.
- Refactor `process_new_files` to add new chunks to the store.

### 2. Tone switcher session-state bug
The tone switcher compares the entire session state object to a string, so the selected tone is never stored correctly (`codex.py` lines 127–137).

*Suggestions*
- Replace `if st.session_state != selected_option:` with `if st.session_state.tone_mode != selected_option:` and ensure `tone_mode` is initialized.
- Display the active tone in the UI for confirmation.

### 3. File uploads lack validation
Uploaded files are written directly to disk without any size or MIME checks, posing security and stability risks (`codex.py` lines 23–29).

*Suggestions*
- Enforce file size limits and check MIME types server‑side.
- Sanitize filenames and store uploads in a temporary directory.
- Provide user feedback when validation fails.

### 4. Missing setup instructions and API key guidance
The README describes design choices and sample interactions but omits environment setup, dependency installation, and API key configuration (`README.md` lines 1–31).

*Suggestions*
- Add a “Getting Started” section with Python version, virtual environment, and `pip install -r requirements.txt` instructions.
- Document required environment variables like `GOOGLE_API_KEY` and how to obtain them.
- Include `streamlit run codex.py` usage instructions and troubleshooting tips.

### 5. No automated tests or linting
The repository includes no tests or linting, making regression detection difficult.

*Suggestions*
- Add a `tests/` directory with unit tests for file handling, PDF ingestion, and tone switching (mocking external APIs).
- Integrate `pytest` and a linter such as `flake8` or `black`, documenting how to run them.
- Optionally configure a GitHub Actions workflow to run checks on pull requests.

## Additional Notes
- `requirements.txt` only lists core dependencies (`requirements.txt` lines 1–3); include testing and linting tools once added.
- The candidate’s submission email provides repository and deployment links but lacks formatting and context (`email-hendrik-raubenheimer.md` line 1).
