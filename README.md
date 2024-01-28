# The Project
## Table of Contents
1. [Overview](#overview)  
  1.1. [Client](#client)  
  1.2. [ Server](#server)  
2. [Client Details](#client-details)  

## Overview
### Client
The client ueses ` requests ` library and ` streamlit `.
it uses request to send http requests to the server and streamlit for the front-end side to show the result and enables the user to write and send the request.
###Server
The server uses flask for the web server to open a port and accept requests. it creates the main http request and sends it to the gemini pro api
it also sends back the response received from google gemini pro api to the client.

## Client Details
```python
  user_input = st.text_area("Enter your request:")
```
this is the text area that the user can write the question to be sent to the server.
```python
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
```
after the submit button is clicked, the request_data is created as a dictionary variable and the "text" key's value is set to the text in the text field.
the other headers of the request is hard coded since I didn't want to user to be bothered witht it, although it can be easily controlled by the user through some sliders and select/options.
```python
  url = 'http://localhost:8000/send_request'
    response = requests.post(url, json=request_data)
```
In this section we initialize a variable named "url" and put the url + port of the server.
then we send a request using the `request` library that we imported to the server ( post method since we want to send something to the server ) and convert the request_data to a json file.
```python
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
```
in this section we display the message by iterating through different sections of the json response message that we received in the client and display the results that we need,
I used this iterative method to improve the visuals of the application.
as you can see if the response status code was 200 which means OK, we display the message and if it was not 200, which means some error has occured, we show an error code and the error message.

