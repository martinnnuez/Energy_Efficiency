import requests

input_example = {
    "X1": 0.68,
    "X2": 423.40,
    "X3": 205.00,
    "X4": 115.55,
    "X5": 6.00,
    "X6": 1,
    "X7": 0.00,
    "X8": 0,
}


url = 'http://localhost:9696/predict'
response = requests.post(url, json=input_example, timeout=5)
print(response.json())
