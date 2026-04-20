import requests
import json

try:
    response = requests.get("https://openrouter.ai/api/v1/models", timeout=15)
    if response.status_code == 200:
        models = response.json().get("data", [])
        ids = [m.get("id") for m in models]
        with open("scripts/models_list.txt", "w") as f:
            for id in sorted(ids):
                f.write(f"{id}\n")
        print(f"Total models found: {len(ids)}. List saved to scripts/models_list.txt")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception: {e}")
