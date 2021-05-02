
if False :
    import wifimgr

    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D
else :
    import network
    import time

    ap_ssid = "macanumdrive"
    ap_password = "macanumdrive"
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=ap_ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=ap_password)  
  
    print('\nConnected. Network config: ', ap_if.ifconfig())
    
    time.sleep(3)


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.


print("ESP OK")
import  startwww
import machine
pin2 = machine.Pin(2, machine.Pin.OUT)
pin2.value(1)
#import webrepl
#webrepl.start()
