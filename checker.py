import requests
import json

# while true
try:
    r = requests.post('http://192.168.100.14/rath-api/sender.php')
    j = json.loads(r.text)
    queues = j['queues']

    for q in queues:
        if q['id'] == '1':
            r = requests.post('http://192.168.100.14/rath-api/sender.php',
            data={'confirm':1})

            #  line api stuff
            msg = q['message']

            break

    print(queues)
except Exception as e:
    print('Error:', e)
