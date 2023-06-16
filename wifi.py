import urllib.request
import time
a=[]
b=[]
send = ''
for i in a:
    send += str(round(i, 3))
    send += 'a'

send += 'b'

for i in b:
    send += b
    send += 'a'

while True:
    urllib.request.urlopen(f'http://192.168.130.253/H')
    time.sleep(0.1)
    urllib.request.urlopen(r'http://192.168.130.253/L')
    time.sleep(0.05)
    