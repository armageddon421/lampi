import socket
import time
import random

UDP_IP = "192.168.1.1"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setblocking(False)
sock.bind(('',0)) #let kernel pick port

data = bytearray(10*12)

# global variables for send_data
packetCounter = 0
lastPacketLossAdjustment = time.time()

def send_data():
    global packetCounter
    global lastPacketLossAdjustment

    try:
        recvbytes, address = sock.recvfrom(3) # try to receive "OK" from lampi
        if(packetCounter > 0):
            packetCounter -= 1
    except:
        #print ("nothing received")
        pass

    if(packetCounter > 0 and time.time() > lastPacketLossAdjustment + 0.25):
        lastPacketLossAdjustment = time.time()
        packetCounter -= 1
    
    if(packetCounter < 20):
        print ("sending")
        sock.sendto(data, (UDP_IP, UDP_PORT))
        packetCounter += 1

    print (packetCounter)
    

def set_pixel(index, color):
    if index < 0: return
    if index >= 12: return

    data[index*10+0] = int(color[0])
    data[index*10+2] = int(color[1])
    data[index*10+4] = int(color[2])
    data[index*10+6] = int(color[3])

def get_pixel(index):
    return (data[index*10+0], data[index*10+2], data[index*10+4], data[index*10+6])


index = 0

while True:

    for i in range(12):
        color = get_pixel(i)
        factor = 0.8
        set_pixel(i, (color[0]*factor, color[1]*factor, color[2]*factor, color[3]*factor))

    if index % 4 == 0:
        set_pixel(random.randint(0,11), (random.randint(0,255),0,random.randint(0,255),random.randint(0,255) ))
    #set_pixel((index//1)%12, (255,0,0,0))

    index += 1

    send_data()

    time.sleep(0.04)
    #time.sleep(0.3)
