import streamlit as st
import requests
from openai import OpenAI

# Hard-coded API key
OPENAI_API_KEY = st.text_input("OpenAI API Key", type="password")
if not OPENAI_API_KEY:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    st.title("Cutomer Complaint Analyser")
    st.write(
        "Enter the URL of a text or Markdown document below, then ask a question about it – GPT will answer!"
    )

    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)


    doc_url = "https://raw.githubusercontent.com/Beingjn/Streamlit_Chatbot_Example/main/report.txt"
    # Fetch the document 
    document = None
    if doc_url:
        try:
            resp = requests.get(doc_url, timeout=10)
            resp.raise_for_status()
            document = resp.text
        except Exception as e:
            st.error(f"Failed to load document: {e}")

    # Ask your question
    question = st.text_area(
        "Ask a question about customer feedback",
        disabled=not bool(document),
    )

    if st.button("Get Answer") and document and question:
        messages = [
            {"role": "system", "content": f"Document context:\n\n{document}"},
            {"role": "user",   "content": question}
        ]
        with st.spinner("Thinking..."):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )
            st.write_stream(stream)