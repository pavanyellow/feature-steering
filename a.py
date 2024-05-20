import requests

resp = requests.post(
    "https://model-e3mv6pz3.api.baseten.co/production/predict",
    headers={"Authorization": "Api-Key Fn7R3A6B.sNl9j0G1rHVCZSjrHHcT6ZAnHsF2T2n8"},
    json={'top_p': 0.75, 'prompt': "What's the meaning of life?", 'num_beams': 4, 'temperature': 0.1},
    stream=True
)

for content in resp.iter_content():
    print(content.decode("utf-8"), end="", flush=True)

