from app.templating import render_file
from app.templating import render_myfile
from app.templating import generate_tname
from app.inventory import parameter_lookup
from fbtftp.base_handler import StringResponseData
from app import configuration as C
import os
import time


class TftpData:

    def __init__(self, filename):
        path = os.path.join(C.TFTP_ROOT, filename)
        self._size = os.stat(path).st_size
        self._reader = open(path, 'rb')

    def read(self, data):
        return self._reader.read(data)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()


def request_dispatcher(file_path):

    if "ZTP" in file_path:
        ztpname = file_path.split('-')[0]
        ztplog = str(ztpname + ".log")
        while os.path.isfile(C.CACHE_DIR + ztplog) is False:
            time.sleep(1)
        with open(os.path.join(C.CACHE_DIR, ztplog), "r") as f:
            cache = f.readline().split(';')
            serial = cache[4]
            devicename = cache[5]
            if devicename == 'UNKNOWN':
                config = render_file('unknownhost-confg', staging_enasec=C.STAGING_ENASEC)
                return StringResponseData(config)
            elif devicename == 'DFAILURE':
                config = render_file('failedhost-confg')
                return StringResponseData(config)
            elif devicename == 'TFAILURE':
                config = render_file('failedhost-confg')
                return StringResponseData(config)
            elif os.path.isfile(C.CONFIG_DIR + devicename):
                with open(os.path.join(C.CONFIG_DIR, devicename), "r") as fh:
                    config = fh.read()
                    return StringResponseData(config)
            else:
                parameters = parameter_lookup(serial)
                config = render_myfile(parameters[0]['template'], parameters[0])
                return StringResponseData(config)

    if file_path == 'network-confg':
        tname = generate_tname()
        config = render_file(file_path, hostname=tname, staging_bn=C.STAGING_BN, staging_pw=C.STAGING_PW, staging_domain=C.STAGING_DOMAIN)
        return StringResponseData(config)

    else:
        return TftpData(file_path)

