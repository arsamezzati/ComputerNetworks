from flask import Flask, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

# fetches the access token
access_token = subprocess.getoutput('gcloud auth print-access-token').strip()


# triggers the send request function
@app.route('/send_request', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=False, port=8000)
