import urllib.request
import time
while True:
    urllib.request.urlopen(f'http://192.168.130.253/H')
    time.sleep(0.1)
    urllib.request.urlopen(r'http://192.168.130.253/L')
    time.sleep(0.05)