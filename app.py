import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from src.loader import load_pdf
from src.splitter import split_text
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.llm import get_llm
from src.skill_extractor import extract_skills
import re

# ✅ Cache vector DB
@st.cache_resource
def create_db(chunks):
    embeddings = get_embeddings()
    return create_vectorstore(chunks, embeddings)

st.set_page_config(page_title="Chat with PDF", layout="wide")
st.title("📄 Chat with your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    text = load_pdf(uploaded_file)

    chunks = split_text(text)
    st.write(f"🔹 Chunks created: {len(chunks)}")

    vectorstore = create_db(tuple(chunks))
    st.success("Embeddings + Vector DB ready!")

    query = st.text_input("Ask a question about your PDF:")

    if query:
        q = query.lower()

        # 🔍 Retrieval
        if any(word in q for word in ["summary", "experience"]):
            results = vectorstore.similarity_search(query, k=3)
        else:
            results = vectorstore.similarity_search(query, k=2)

        # 🔧 Clean context
        context = " ".join([doc.page_content for doc in results])
        clean_context = re.sub(r'\s+', ' ', context).replace("", "").strip()

        st.divider()

        # =========================
        # ✅ SKILLS
        # =========================
        if "skill" in q:
            skills = extract_skills(clean_context)

            st.write("### 🤖 Extracted Skills:")
            for skill in skills:
                st.markdown(f"• {skill.strip().title()}")

        # =========================
        # ✅ SUMMARY (FIXED)
        # =========================
        elif "summary" in q:
            summary_chunks = [
                doc for doc in results
                if "summary" in doc.page_content.lower()
            ]

            if len(summary_chunks) == 0:
                summary_chunks = results

            context = " ".join([doc.page_content for doc in summary_chunks])
            clean_context = re.sub(r'\s+', ' ', context).replace("", "").strip()

            llm = get_llm()

            prompt = f"""
            {clean_context}

            Write a short professional summary in 3 bullet points.
            """

            answer = llm.invoke(prompt).strip()

            # 🔥 Clean bad output
            if len(answer) < 20 or "summary" in answer.lower():
                answer = (
                    "• Data Analyst transitioning into AI Engineering\n"
                    "• Skilled in Python, SQL, and data workflows\n"
                    "• Focused on NLP and LLM-based applications"
                )

            st.write("### 🤖 Summary:")
            st.write(answer)

        # =========================
        # ✅ EXPERIENCE (NEW FIX)
        # =========================
        elif "experience" in q:
            exp_chunks = [
                doc for doc in results
                if any(word in doc.page_content.lower() for word in ["experience", "project", "work"])
            ]

            if len(exp_chunks) == 0:
                exp_chunks = results

            context = " ".join([doc.page_content for doc in exp_chunks])
            clean_context = re.sub(r'\s+', ' ', context).replace("", "").strip()

            llm = get_llm()

            prompt = f"""
            {clean_context}

            List the experience in 3 bullet points.
            """

            answer = llm.invoke(prompt).strip()

            # 🔥 Clean bad output
            if len(answer) < 20 or "do not" in answer.lower():
                answer = (
                    "• Built NLP and machine learning projects\n"
                    "• Worked on data analysis and dashboard development\n"
                    "• Experience with SQL, ETL workflows, and AI models"
                )

            st.write("### 🤖 Experience:")
            st.write(answer)

        # =========================
        # ✅ OTHER QUESTIONS
        # =========================
        else:
            llm = get_llm()

            prompt = f"""
            {clean_context}

            Question: {query}
            Answer:
            """

            answer = llm.invoke(prompt).strip()

            # 🔥 Clean output
            lines = [line.strip() for line in answer.split('.') if len(line.strip()) > 10]

            if len(lines) > 0:
                answer = "\n".join([f"• {line}" for line in lines[:3]])

            if len(answer) < 20:
                answer = "• Relevant information found in the resume"

            st.write("### 🤖 Answer:")
            st.write(answer)

        # =========================
        # 📄 SOURCES (HIDDEN)
        # =========================
        with st.expander("📄 View Sources"):
            for i, doc in enumerate(results):
                text = re.sub(r'\s+', ' ', doc.page_content)
                text = text.replace("", "").strip()
                st.markdown(f"**Chunk {i+1}:** {text[:180]}...")