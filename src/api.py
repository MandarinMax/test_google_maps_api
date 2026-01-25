# src/api.py
import requests

def get_data():
    response = requests.get("http://example.com")
    response.raise_for_status()
    return response.json()