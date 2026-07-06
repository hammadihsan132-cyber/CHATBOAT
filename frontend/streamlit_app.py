import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="centered")

st.title("💬 Gemini Chatbot")
st.caption("Powered by Gemini via FastAPI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption(f"Messages in conversation: {len(st.session_state.messages)}")

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"messages": st.session_state.messages},
                    timeout=30
                )
                response.raise_for_status()
                answer = response.json()["response"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except requests.exceptions.ConnectionError:
                error_msg = "⚠️ Can't connect to the server. Is FastAPI running on port 8000?"
                st.error(error_msg)

            except requests.exceptions.Timeout:
                error_msg = "⚠️ The request timed out. Try again."
                st.error(error_msg)

            except requests.exceptions.HTTPError:
                if response.status_code == 503:
                    error_msg = "⚠️ Gemini is currently overloaded. Please try again shortly."
                else:
                    error_msg = f"⚠️ Server error ({response.status_code}): {response.text}"
                st.error(error_msg)

            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")