# The Project
## Table of Contents
1. [Overview](#overview)  
  1.1. [Client](#client)  
  1.2. [ Server](#server)  
2. [Client Details](#client-details)
3. [Server Details](#server-details)

## Overview
### Client
The client ueses ` requests ` library and ` streamlit `.
it uses request to send http requests to the server and streamlit for the front-end side to show the result and enables the user to write and send the request.
### Server
The server uses flask for the web server to open a port and accept requests. it creates the main http request and sends it to the gemini pro api
it also sends back the response received from google gemini pro api to the client.

## Client Details
```python
  # initializing the session if not exists already
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
```
this is a session which is used in streamlit to keep state. 

```python
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
```
Whenver user prompt is submitted ( by pressing enter ), this block of code checks if it is null or not and creates a request. the first like also creates the chat_input section.

```python
  url = 'http://localhost:8000/send_request'
    response = requests.post(url, json=request_data)
```
In this section we initialize a variable named "url" and put the url + port of the server.
then we send a request using the `request` library that we imported to the server ( post method since we want to send something to the server ) and convert the request_data to a json file.
```python
     if response.status_code == 200:
        response_data = response.json()
        # saving the response to history
        st.session_state.conversation_history.append((prompt, response_data))

        # displaying old and new Q/A by iterating through the key value pair
        for prompt, response in st.session_state.conversation_history:

            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                for item in response:
                    for candidate in item.get("candidates", []):
                        content = candidate.get("content", {})
                        text_parts = content.get("parts", [])

                        for part in text_parts:
                            text = part.get("text", "")
                            st.write(text)

    else:
        st.error(f"Failed to get response. Status code: {response.status_code}")
```
in this section, the application checks the response from server.py, if the response code was 200 ( OK ) it adds the key value pair of prompt and response. then iterate through it to show ever Q & A since the application started.
if it wasn't 200, it shows the error code instead and doesn't add anything else.
## Server Details
```python
app = Flask(__name__)
```
this section initiated the flask web server.
```python
@app.route('/send_request', methods=['POST'])
def send_request():
```
The first line triggeres the function directly below it whenever a post request is sent to the localhost:8000/send_request URL, which means the send_request() function
```python
def send_request():
    try:
        # gets json data ( handles incoming request )
        request_data = request.json

        # api endpoint
        url = ("https://us-central1-aiplatform.googleapis.com/v1/projects/networks-412412/locations/us-central1"
               "/publishers/google/models/gemini-pro:streamGenerateContent")

        # defining the headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        # uses requests library to post and get the response and put it in a variable
        response = requests.post(url, headers=headers, json=request_data)
```
In this section when the function is triggered, the request file is put into a variable, then we define the url for our server request message and our headers `Authorization` and `Content-Type`.
we use our access token variable which is defined earlier.
```python
access_token = subprocess.getoutput('gcloud auth print-access-token').strip()

```
This line gets the access token by using subprocess.getoutput which basically lets us run an OS command in python. we then put the command we want to run in the terminal in the argument section. thne we use the `strip()` method to remove any possible white-space.

```python
response = requests.post(url, headers=headers, json=request_data)

        if response.status_code == 200:
            # Save the response to response.json file
            response_json = response.json()
            with open('response.json', 'w') as file:
                json.dump(response_json, file, indent=4)

            # Send the response.json file back to the client
            return jsonify(response_json)
        else:
            return jsonify({"error": "Failed to get a valid response from the API."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

```
this sections sends and receives the http request/message,
if the response code was 200, it turns it into a dictionary format using .json() method and then creates a json file and sends it back to the client using `return jsonify(response_json)`.
if not it returns the error.
