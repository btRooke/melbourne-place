import network, webrepl

SSID = "Matt LANcock"
PASS = "quoththeravennevermore"

webrepl.start()

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    print("Connecting to network")
    sta_if.active(True)
    sta_if.connect(SSID, PASS)
    
    while not sta_if.isconnected():
        pass

print("Connected to network:", sta_if.ifconfig())