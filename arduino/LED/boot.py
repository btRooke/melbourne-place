from network import WLAN, STA_IF
from webrepl import start as webrepl_start
from setup_net import SSID, PASS

if __name__ == "__main__":
    webrepl_start()
    sta_if = WLAN(STA_IF)

    if not sta_if.isconnected():
        print("Connecting to network")
        sta_if.active(True)
        sta_if.connect(SSID, PASS)
        
        while not sta_if.isconnected():
            pass

    print("Connected to network:", sta_if.ifconfig())