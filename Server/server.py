from flask import Flask, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

# Function to get the access token
def get_access_token():
    # Run the 'gcloud auth print-access-token' command and get the output
    access_token = subprocess.getoutput('gcloud auth print-access-token')
    print(access_token.strip())
    return access_token.strip()

access_token = get_access_token()

@app.route('/send_request', methods=['POST'])
def send_request():
    try:
        # Get JSON data from the request
        request_data = request.json

        # URL of the API endpoint
        url = "https://us-central1-aiplatform.googleapis.com/v1/projects/networks-412412/locations/us-central1/publishers/google/models/gemini-pro:streamGenerateContent"

        # Headers for the request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        # Send the POST request
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
    app.run(debug=True, port=8000)
