import requests
import json

# while true
try:
    r = requests.post('http://192.168.100.14/rath-api/api.php', data={'confirm':4})

    j = json.loads(r.text)
    queues = j['queues']

    print(queues)
except Exception as e:
    print('Error:', e)