import streamlit as st
import requests

API_URL = "http://localhost:8000/api/research"

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
    .summary-card { background: #f8fafc; border-left: 4px solid #3b82f6; padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1rem; }
    .chat-user { background: #1c2b4a; color: white; padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 0.5rem; }
    .chat-assistant { background: #f1f5f9; padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 1rem; color: #1c2b4a; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔬 AI Research Assistant")
st.markdown("Upload a research paper and chat with it using AI")

if 'paper_id' not in st.session_state:
    st.session_state.paper_id = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'filename' not in st.session_state:
    st.session_state.filename = None

with st.sidebar:
    st.header("📄 Upload Paper")
    uploaded_file = st.file_uploader("Choose a PDF", type=['pdf'])

    if uploaded_file and uploaded_file.name != st.session_state.filename:
        with st.spinner("🔍 Processing paper..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.paper_id = data['paper_id']
                    st.session_state.summary = data['summary']
                    st.session_state.chat_history = []
                    st.session_state.filename = uploaded_file.name
                    st.success(f"✅ Processed {data['num_chunks']} chunks!")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

    if st.session_state.paper_id:
        st.divider()
        st.success(f"📖 **{st.session_state.filename}**")
        if st.button("🗑️ Clear Paper"):
            requests.delete(f"{API_URL}/delete",
                json={"paper_id": st.session_state.paper_id})
            st.session_state.paper_id = None
            st.session_state.summary = None
            st.session_state.chat_history = []
            st.session_state.filename = None
            st.rerun()

    st.divider()
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "What is the main contribution?",
        "What dataset was used?",
        "What are the key results?",
        "What are the limitations?",
        "How does this compare to prior work?"
    ]
    for q in sample_questions:
        if st.button(q, key=q):
            st.session_state.selected_question = q

if st.session_state.paper_id and st.session_state.summary:
    summary = st.session_state.summary

    st.subheader(f"📋 {summary.get('title', 'Research Paper')}")

    st.markdown(f"""
    <div class="summary-card">
    <strong>📝 Overview</strong><br>{summary.get('summary', 'N/A')}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Chat Section
    st.subheader("💬 Chat with the Paper")

    for chat in st.session_state.chat_history:
        st.markdown(f'<div class="chat-user">🧑 {chat["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-assistant">🤖 {chat["answer"]}</div>', unsafe_allow_html=True)

    default_q = st.session_state.get('selected_question', '')
    question = st.text_input("Ask a question about the paper:", value=default_q, placeholder="e.g. What are the key contributions?")

    col1, col2 = st.columns([1, 5])
    with col1:
        ask_btn = st.button("Ask 🚀", use_container_width=True)
    with col2:
        if st.button("Clear Chat 🗑️"):
            st.session_state.chat_history = []
            st.rerun()

    if ask_btn and question.strip():
        with st.spinner("🧠 Thinking..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={
                    "paper_id": st.session_state.paper_id,
                    "question": question
                })
                if response.status_code == 200:
                    answer = response.json()['answer']
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })
                    if 'selected_question' in st.session_state:
                        del st.session_state.selected_question
                    st.rerun()
                else:
                    st.error(f"Error: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.markdown("""
    <div style="text-align:center; padding: 5rem 2rem;">
        <h2 style="color:#6b7280;">👈 Upload a research paper to get started</h2>
        <p style="color:#9ca3af;">Supports any PDF research paper — just drag and drop!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📄 **Upload any PDF**\nResearch papers, articles, or academic documents")
    with col2:
        st.info("🤖 **AI Analysis**\nAuto-generates a summary of the paper")
    with col3:
        st.info("💬 **Chat with it**\nAsk any question and get cited answers")