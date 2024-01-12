import requests
import json
import argparse

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-m", "--model", help="llm model", type=str, default="tinyllama")
parser.add_argument("-p", "--prompt", help="model prompt", type=str, required=True)

# Read arguments from command line
args = parser.parse_args()

url = "http://localhost:11434/api/generate"

# Define the payload (data to be sent with the request)
payload = {
    "model": args.model,
    "prompt": args.prompt
}

# Send the POST request with streaming
with requests.post(url, json=payload, stream=True) as response:
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Iterate through the streaming responses
        for line in response.iter_lines():
            if line:
                # Parse the JSON response
                data = json.loads(line.decode("utf-8"))
                
                # Print without buffering
                print(data["response"], end="", flush=True)
        print("")
    else:
        print(f"Error: {response.status_code} - {response.text}")
