import network
import webrepl
import time

ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.config(
    essid="ERC_Classroom",
    password="12345678",
    authmode=network.AUTH_WPA_WPA2_PSK
)

print("Access Point Started")
print("IP Address:", ap.ifconfig()[0])

webrepl.start()
