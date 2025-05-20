from app.templating import render_file
from app.templating import generate_tname
from app.notifications import notify_syslog
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

    if file_path == 'network-confg':
        tname = generate_tname()
        os.environ['TNAME'] = str(tname)
        config = render_file('network-confg', hostname=tname, staging_bn=C.STAGING_BN, staging_pw=C.STAGING_PW, staging_domain=C.STAGING_DOMAIN)
        if config not in ['','T68','T74','T81','T82']:
            return StringResponseData(config)

    elif "ZTP" in file_path:
        ztpname = file_path.split('-')[0]
        cachefile = str(ztpname + ".log")
        timeout = 30
        i = 1
        while i != timeout and os.path.isfile(C.CACHE_DIR + cachefile) is False:
            time.sleep(1)
            i += 1
        if i == timeout:
            notify_syslog(f"{ztpname} dispatcher timeout getting cache")
            config = render_file('failedhost-confg')
        else:
            with open(os.path.join(C.CACHE_DIR, cachefile), "r") as f:
                cache = f.readline().split(';')
                i = 1
                while i != timeout and len(cache) < 6:
                    time.sleep(1)
                    cache = f.readline().split(';')
                    i += 1
                if i == timeout:
                    notify_syslog(f"{ztpname} dispatcher timeout getting devicename from cache")
                    devicename = 'CFAILURE'
                else:
                    devicename = cache[5]
            if devicename == 'CFAILURE':
                config = render_file('failedhost-confg')
            elif devicename == 'CONFAILURE':
                config = render_file('failedhost-confg')
            elif devicename == 'DFAILURE':
                config = render_file('failedhost-confg')
            elif devicename == 'TFAILURE':
                config = render_file('failedhost-confg')
            elif devicename == 'UNKNOWN':
                config = render_file('unknownhost-confg', staging_enasec=C.STAGING_ENASEC)
            else:
                with open(os.path.join(C.CACHE_DIR, cachefile), "r") as f:
                    cache = f.read().split(';')
                    i = 1
                    while i != timeout and len(cache) < 7:
                        time.sleep(1)
                        cache = f.read().split(';')
                        i += 1
                if i == timeout:
                    notify_syslog(f"{ztpname} dispatcher timeout getting config from cache")
                    config = render_file('failedhost-confg')
                else:
                    config = cache[6]
        if config not in ['','T68','T74','T81','T82']:
            return StringResponseData(config)

    else:
        if os.path.isfile(C.TFTP_ROOT + file_path):
            return TftpData(file_path)

