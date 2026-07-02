import streamlit as st
from ollama_client import ask_ollama

from rubrik_service import (
    get_protected_vms,
    get_protection_summary,
    get_replication_failures,
    get_latest_recovery_points,
    get_vm_recovery_point
)

st.set_page_config(
    page_title="DRaaS AI Assistant",
    layout="wide"
)

st.title("DRaaS AI Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask a DR question..."
)

if question:
    
st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
    response = ask_ollama(question)
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.stop()

    try:

        q = question.lower().strip()

        response = ""

        # Protected VMs
        if (
            "protected vm" in q
            or "protected vms" in q
            or "which vms are protected" in q
            or "what are the vms that are protected" in q
            or "list protected vms" in q
        ):

            response = get_protected_vms()

        # Summary
        elif (
            "summary" in q
            or "health" in q
            or "readiness" in q
            or "protection summary" in q
        ):

            response = get_protection_summary()

        # Replication Failures
        elif (
            "replication" in q
            and "failure" in q
        ):

            response = get_replication_failures()

        # Recovery Points
        elif (
            "recovery point" in q
            or "recovery points" in q
        ):

            vm_name = (
                q.replace("show", "")
                 .replace("latest", "")
                 .replace("what is the", "")
                 .replace("recovery points", "")
                 .replace("recovery point", "")
                 .replace("for", "")
                 .replace("?", "")
                 .strip()
            )

            if vm_name:
                response = get_vm_recovery_point(vm_name)
            else:
                response = get_latest_recovery_points()

        else:

            response = """
Supported Questions:

• Show protected VMs

• What are the VMs that are protected?

• Show protection summary

• Any replication failures?

• Show recovery points

• Show recovery point for draas-win-vm1
"""

    except Exception as ex:

        response = f"Error: {str(ex)}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
