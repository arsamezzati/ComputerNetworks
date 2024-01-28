import streamlit as st
import requests

st.title('Send Request to Server')

# initializing the session so the previous messages would show up after asking a new one
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
# this happens when user presses Enter
if prompt := st.chat_input("Ask your question, press Enter to submit"):
    request_data = {
        "contents": {
            "role": "user",
            "parts": prompt
        },
        "safety_settings": {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        "generation_config": {
            "temperature": 0.9,
            "topP": 1.0,
            "maxOutputTokens": 2048
        }
    }
    url = 'http://localhost:8000/send_request'
    response = requests.post(url, json=request_data)

    # checking the response code and displaying the Q/A
    if response.status_code == 200:
        response_data = response.json()
        # adds the question + answer to the session.
        st.session_state.conversation_history.append((prompt, response_data))

        # it shows the history + new Q/A
        for prompt, response in st.session_state.conversation_history:

            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                for item in response:  # Assuming response is a list of items
                    for candidate in item.get("candidates", []):
                        content = candidate.get("content", {})
                        text_parts = content.get("parts", [])

                        for part in text_parts:
                            text = part.get("text", "")
                            st.write(text)

    else:
        st.error(f"Failed to get response. Status code: {response.status_code}")
