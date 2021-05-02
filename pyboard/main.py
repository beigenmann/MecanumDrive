
if False :
    import wifimgr

    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D
else :
    import network

    ap_ssid = "macanumdrive"
    ap_password = "macanumdrive"
    ap_authmode = 3  # WPA2
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ap_ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=ap_password)  


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
import  startwww
#import webrepl
#webrepl.start()
