from ota import OTAUpdater
from secrets import SSID, PASSWORD

firmware_url = "https://github.com/maiconDuarte/IoT_OTA/main"
ota_updater = OTAUpdater(secrets.SSID, secrets.PASSWORD, firmware_url, "iot_main.py")
ota_updater.download_and_install_update_if_available()
