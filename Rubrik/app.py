import streamlit as st

from ollama_client import ask_ollama

st.set_page_config(
    page_title="DRaaS AI Assistant",
    layout="wide"
)

st.title("DRaaS AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask a DR question...")

if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:

        # Send question to Ollama
        response = ask_ollama(question)

    except Exception as ex:

        response = f"Error connecting to Ollama:\n\n{str(ex)}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
