import board
import busio
import digitalio
import time

import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from lib.adafruit_requests import OutOfRetries


##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

##reset
W5x00_RSTn = board.GP20

print("Wiznet5k Web Client (P2P)")

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x01, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 2, 2)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = ()
DNS_SERVER = ()

CLIENT_IP = '192.168.2.1'

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(SPI0_CSn)

# cs = digitalio.DigitalInOut(board.D5)
spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset W5500 first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# Initialize ethernet interface without DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
# Initialize ethernet interface with DHCP
# eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

# Set network configuration
eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Initialize a requests object with a socket and ethernet interface
requests.set_socket(socket, eth)

# Here we create our application, registering the
# following functions to be called on specific HTTP GET requests routes

while True:

    attempts = 3  # Number of attempts to retry each request
    failure_count = 0
    r = None

    while not r:
        try:
            print("Fetching text from", CLIENT_IP)
            r = requests.get(f'http://{CLIENT_IP}')
            print("-" * 40)
            print(dir(r))
            print("-" * 40)
            r.close()
            time.sleep(2)
        except OutOfRetries:
            print("Request failed, retrying...\n")
            failure_count += 1
            if failure_count >= attempts:
                raise AssertionError("Something went wrong. Please \
                    connect server and client again") 
        continue
