# lampi
This repository contains python code to send data to lampi

Lampi is a light fixture with 12 independent glass spheres. Each sphere can show RGBW color with up to 12 bit per channel.

Lampi contains an esp8266 WiFi chip. You can connect to it's WiFi access point and stream data via UDP. If no data is received for two seconds, lampi shows it's default standby animation.

## How to connect
If you're on the 36th chaos communication congress, you can find lampi in the kitchen cube between halls 3 and 5. Connect to the hotspot "lampi" using the password "lampi36c3". Send exactly 120 bytes of data to UDP port 1234 on 192.168.1.1. Receive response packets on the port you're sending from.

## data format

Each sphere takes 10 bytes of data. 2 bytes for each color (red, green, blue and white) and two bytes for effects. This makes it a total of 12*10=120 bytes.

# using the example code

The example code abstracts setting and getting colors for specific spheres as well as sending the data to lampi via UDP. It counts responses and stops sending if too many responses are missing. To account for packet loss, that counter is also reduced at a set interval.

No specific python version is required to run the scripts, they should work on python 2 and 3. 

main.py has no additional dependencies.

main_pygame.py shows current colors and creates a strobe on mouse click/touch. It requires pygame to run.

Both scripts also run on android using QPython (not sure about QPython3)
