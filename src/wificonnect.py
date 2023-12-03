import pywifi
from pywifi import const
import time

#wifi settings
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
Name = iface.name()

#profie
profile = pywifi.Profile()
profile.ssid = "kuas-wlan"
profile.auth = const.AUTH_ALG_OPEN
profile.akm.append(const.AKM_TYPE_WPA2PSK)
profile.cipher = const.CIPHER_TYPE_CCMP
profile.key = "Kyotosentan2019"

profile = iface.add_network_profile(profile)
iface.connect(profile)

time.sleep(1)
if iface.status() == const.IFACE_CONNECTED:
    print("接続成功")
else:
    print("接続失敗")