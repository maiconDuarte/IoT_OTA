from ota import OTAUpdater
import secrets

firmware_url = "https://github.com/maiconDuarte/IoT_OTA/"

ota_updater = OTAUpdater(secrets.SSID, secrets.PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()
