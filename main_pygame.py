#qpy:pygame

import socket
import time
import random

import pygame


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


    
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
    

index = 0

while True:

    screen.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                pygame.draw.circle(screen, (255,255,255), event.pos, 10)
                for i in range(12):
                    color = (255,255,255,255)
                    set_pixel(i, (color[0], color[1], color[2], color[3]))
  

    for i in range(12):
        color = get_pixel(i)
        factor = 0.8
        set_pixel(i, (color[0]*factor, color[1]*factor, color[2]*factor, color[3]*factor))

    if index % 4 == 0:
        set_pixel(random.randint(0,11), (random.randint(0,255),0,random.randint(0,255),random.randint(0,255) ))
    #set_pixel((index//1)%12, (255,0,0,0))

    index += 1

    send_data()
    
    
    radius = int(screen.get_size()[0]/6/2)
    pos = [radius*3,0]
    for i in range(12):
        color = get_pixel(i)
        dispcolor = (color[0]/2+color[3]/2, color[1]/2+color[3]/2, color[2]/2+color[3]/2)

        
        if(i == 3 or i == 9):
            pos[1] += radius*2
        if(i == 3):
            pos[0] = 0
        if(i == 9):
            pos[0] = radius*3

                
        pygame.draw.circle(screen, dispcolor, (pos[0]+radius,pos[1]+radius) , radius)
        pygame.draw.circle(screen, (50,50,50), (pos[0]+radius,pos[1]+radius) , radius,1)
        pos[0] += radius*2
    
    pygame.display.update()
    clock.tick(30)
    #time.sleep(0.04)
    #time.sleep(0.3)
