# Text Chunking Web App using NLTK Sentence Tokenizer

# Step 1: Import Libraries & Streamlit Configuration
import streamlit as st
import nltk
from PyPDF2 import PdfReader

nltk.download("punkt")
nltk.download("punkt_tab")

st.set_page_config(
    page_title="Text Chunking using NLTK",
    layout="wide"
)

st.title("Text Chunking using NLTK Sentence Tokenizer")
st.write("Upload a PDF file to extract text and perform sentence-based semantic chunking.")

# Step 2: Upload & Extract PDF Text
uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        if not extracted_text.strip():
            st.warning("No readable text found in the PDF.")
        else:
            # Step 3: Sentence Tokenization
            sentences = nltk.sent_tokenize(extracted_text)

            st.subheader("Extracted Text Sample (Sentence Index 58 to 68)")

            for i in range(58, min(68, len(sentences))):
                st.markdown(f"**Sentence {i}:** {sentences[i]}")

            # Step 4: Semantic Sentence Chunking
            st.subheader("Semantic Sentence Chunking Result")

            chunks = sentences[58:68]

            for idx, chunk in enumerate(chunks, start=58):
                st.markdown(f"**Chunk {idx}:** {chunk}")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")

else:
    st.info("Please upload a PDF file to proceed.")
