import requests

# Define the API endpoint
url = "http://127.0.0.1:8002/predict"

# Sample paragraph
paragraph = """On the edge of a small,
misty island stood a little lighthouse named Lumy. 
Unlike the towering lighthouses that stretched into the clouds, 
Lumy was small and a bit crooked, with its paint chipped and its light not as bright as others. 
But Lumy had one thing the others didn't: an unshakable determination to help sailors find their way."""

# Create the request payload
payload = {"paragraph": paragraph}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    print(response.json())  # This will contain the allTagData output
else:
    print("Error:", response.status_code, response.text)
