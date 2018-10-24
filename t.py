import requests

response = requests.post('http://localhost:8000/pointcalc').text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
iv_list = [int(i) for i in response.split()]
print(iv_list)
