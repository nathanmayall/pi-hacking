import board
import busio
import digitalio
import time
import supervisor

import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import *
from adafruit_wsgi.wsgi_app import WSGIApp
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

##reset
W5x00_RSTn = board.GP20

print("Wiznet5k Web Server (P2P)")

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x11, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 2, 1)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = ()
DNS_SERVER = ()

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
web_app = WSGIApp()

html_string = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
     vjg rcuuyqtf ku ocvej 
    </body>
    </html>
    '''

#HTTP Request handler
@web_app.route("/")
def root(request):  # pylint: disable=unused-argument
    return ("200 OK", [('Content-type', 'text/html'), ('Content-Length', f'{len(html_string.encode("utf-8"))}')], [html_string])

# Here we setup our server, passing in our web_app as the application
server.set_interface(eth)
wsgiServer = server.WSGIServer(80, application=web_app)

print("Open this IP in your browser: ", eth.pretty_ip(eth.ip_address))

# Start the server
try:
    # Start the server
    wsgiServer.start()
except Exception as e:
    print(e)
    supervisor.reload()

while True:
    # Our main loop where we have the server poll for incoming requests
    try:
        wsgiServer.update_poll()
    except:
        time.sleep(1)
    # Maintain DHCP lease
    # eth.maintain_dhcp_lease()
    # Could do any other background tasks here, like reading sensors