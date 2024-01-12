import requests
import json
import argparse

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-m", "--model", help="llm model", type=str, default="tinyllama")
parser.add_argument("-p", "--prompt", help="model prompt", type=str, required=False)

# Read arguments from command line
args = parser.parse_args()

SERVER_URL = "http://localhost:11434"

def generate_response(prompt, model='tinyllama', context=[]):
    API_END = "/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "context": context
    }

    url = SERVER_URL + API_END
    next_context = []

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
                    if data["done"]: 
                        next_context = data["context"]

        else:
            print(f"Error: {response.status_code} - {response.text}")

    return next_context
 
n = 4
cont = []
while(n):
    promp = input("\n>>> ")
    cont = generate_response(promp, args.model, cont)
    n -= 1
