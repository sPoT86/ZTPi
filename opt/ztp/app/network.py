from napalm import get_network_driver
from app import configuration as C
import time

def get_napalm_connection(host, device_type, attempts=120, timeout=1):
    driver = get_network_driver(device_type)
    device = driver(hostname=host, username=C.STAGING_BN,
                    password=C.STAGING_PW)

    for _ in range(attempts):
        try:
            device.open()
            return device
        except:
            time.sleep(timeout)

    return False
