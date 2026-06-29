import streamlit as st
import tempfile
import os
from datetime import datetime
from pypdf import PdfReader

from pdf_utils import extract_text_from_pdf, split_text
from rag import retrieve_relevant_chunks, ask_gemini

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="DocuTrust",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------

if os.path.exists("style.css"):
    with open("style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "processed" not in st.session_state:
    st.session_state.processed = False

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.markdown("# 🌸 DocuTrust")

    st.markdown(
        """
AI Powered Document Assistant

Upload any PDF and ask unlimited questions.
"""
    )

    st.divider()

    st.subheader("✨ Features")

    st.success("📄 PDF Upload")

    st.success("🤖 Gemini AI")

    st.success("🔎 Intelligent Retrieval")

    st.success("💬 Chat History")

    st.success("⚡ Fast Answers")

    st.divider()

    st.subheader("👩‍💻 Developer")

    st.write("**Ananya Patel**")

    st.write("VIT Vellore")

    st.write("Information Security")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.success("Chat Cleared!")

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
"""
<div class='mainTitle'>
📄 DocuTrust
</div>

<div class='subtitle'>
AI Powered Intelligent Document Question Answering System
</div>
""",
unsafe_allow_html=True
)

st.markdown("---")
# -------------------------------------------------
# UPLOAD CARD
# -------------------------------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📂 Upload your PDF",
    type=["pdf"],
    help="Upload any PDF document to start asking questions."
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# PROCESS PDF
# -------------------------------------------------

if uploaded_file is not None:

    if (
        st.session_state.file_name != uploaded_file.name
        or not st.session_state.processed
    ):

        with st.spinner("📄 Processing document..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.read())

                temp_path = tmp.name

            # Read PDF

            reader = PdfReader(temp_path)

            st.session_state.pages = len(reader.pages)

            # Extract Text

            text = extract_text_from_pdf(temp_path)

            # Chunking

            chunks = split_text(text)

            st.session_state.chunks = chunks

            st.session_state.file_name = uploaded_file.name

            st.session_state.processed = True

            os.remove(temp_path)

        st.success("✅ Document processed successfully!")

# -------------------------------------------------
# DOCUMENT INFORMATION
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("## 📊 Document Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            label="📄 Pages",
            value=st.session_state.pages
        )

    with col2:

        st.metric(
            label="📚 Chunks",
            value=len(st.session_state.chunks)
        )

    with col3:

        st.metric(
            label="🕒 Uploaded",
            value=datetime.now().strftime("%H:%M")
        )

    st.markdown("---")

    st.markdown(
        f"""
<div class='card'>

### 📁 Current Document

**Filename:** {st.session_state.file_name}

This document has been successfully processed and is ready for question answering.

</div>
""",
        unsafe_allow_html=True
    )
    # -------------------------------------------------
# QUESTION SECTION
# -------------------------------------------------

if st.session_state.processed:

    st.markdown("## 💜 Ask Your Question")

    question = st.text_input(
        "",
        placeholder="Example: What is Data Privacy?"
    )

    ask_button = st.button(
        "✨ Get Answer",
        use_container_width=True
    )

    if ask_button:

        if question.strip() == "":

            st.warning("⚠ Please enter a question.")

        else:

            with st.spinner("🤖 Gemini is analyzing your document..."):

                relevant_chunks = retrieve_relevant_chunks(
                    st.session_state.chunks,
                    question,
                    top_k=5
                )

                answer = ask_gemini(
                    relevant_chunks,
                    question
                )

            # -----------------------------------------
            # SAVE CHAT
            # -----------------------------------------

            st.session_state.chat_history.append({

                "question": question,

                "answer": answer,

                "chunks": relevant_chunks

            })

            # -----------------------------------------
            # ANSWER CARD
            # -----------------------------------------

            st.markdown("## 🤖 AI Answer")

            st.markdown(

                f"""

<div class="answer">

{answer}

</div>

""",

                unsafe_allow_html=True

            )

            st.markdown("")

            # -----------------------------------------
            # CONTEXT
            # -----------------------------------------

            with st.expander(
                "📚 View Retrieved Context",
                expanded=False
            ):

                for i, chunk in enumerate(relevant_chunks):

                    st.markdown(

                        f"""

<div class="context">

### 📄 Chunk {i+1}

{chunk}

</div>

""",

                        unsafe_allow_html=True

                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------

if len(st.session_state.chat_history) > 0:

    st.markdown("---")

    st.markdown("## 💬 Chat History")

    for index, chat in enumerate(reversed(st.session_state.chat_history), start=1):

        with st.container():

            st.markdown(
                f"""
<div class='chatUser'>

<b>🙋 You</b>

{chat["question"]}

</div>
""",
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
<div class='chatBot'>

<b>🤖 DocuTrust AI</b>

{chat["answer"]}

</div>
""",
                unsafe_allow_html=True
            )

            with st.expander(f"📚 Source Context #{index}"):

                for i, chunk in enumerate(chat["chunks"], start=1):

                    st.markdown(
                        f"""
<div class='context'>

<b>Chunk {i}</b>

{chunk}

</div>
""",
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# EMPTY STATE
# -------------------------------------------------

if not st.session_state.processed:

    st.markdown("""

<br><br>

<div class='card'>

<h2 align='center'
style='
color:#6B21A8;
font-weight:700;
'>
🌸 Welcome to DocuTrust 🌸
</h2>

<p align='center'>

Upload any PDF to begin asking questions.

This application uses:

✔ Gemini 2.5 Flash

✔ Intelligent Retrieval

✔ AI Question Answering

✔ TF-IDF Search

</p>

</div>

""", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>

<hr>

<h4>💜 DocuTrust</h4>

AI Powered Intelligent Document Question Answering System

<br>

Made with ❤️ using

<b>Python • Streamlit • Gemini AI • Scikit-Learn</b>

<br><br>



</div>
""", unsafe_allow_html=True)