import streamlit as st
import requests


st.title('Send Request to Server')


# user input text-field
user_input = st.text_area("Enter your request:")


if st.button('Submit'):
    # creating the json file after submit button is clicked
    request_data = {
        "contents": {
            "role": "user",
            "parts": {
                "text": user_input
            }
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

    # for displaying the actual json file
    # st.json(request_data)

    # sending the json to the server
    url = 'http://localhost:8000/send_request'
    response = requests.post(url, json=request_data)

    # displaying the response
    if response.status_code == 200:
        st.success("Results: ")
        response_data = response.json()
        for item in response_data:
            for candidate in item.get("candidates", []):
                content = candidate.get("content", {})
                text_parts = content.get("parts", [])
                for part in text_parts:
                    text = part.get("text", "")
                    st.write(text)
    else:
        st.error(f"Failed to get response. Status code: {response.status_code}")
