from app.network import get_napalm_connection
from app.templating import render_file
from app.notifications import notify_im
from app.notifications import notify_syslog
from app.inventory import parameter_lookup
from app import configuration as C
import os
import datetime
import time


def ztp_start(host, file):
    msg = f"{host} downloaded {file}"
    notify_syslog(msg)
    notify_im(msg)
    if file == 'network-confg':
        dev = get_napalm_connection(host, 'ios')
        if dev:
            msg = f"{host} connection established"
            notify_syslog(msg)
            facts = dev.get_facts()
            msg = f"{host} {facts['hostname']}/{facts['model']}/{facts['serial_number']}"
            notify_syslog(msg)
            cachefile = str(facts['hostname'] + ".log")
            parameters = parameter_lookup(facts['serial_number'])
        else:
            msg = f"{host} connection failed"
            notify_syslog(msg)
            cachefile = str(os.environ.get('TNAME') + ".log")
            parameters = 'C18'
        dtime = datetime.datetime.now()
        with open(os.path.join(C.CACHE_DIR, cachefile), "w") as fh:
            if parameters == 'C18':
                logentry = f"{dtime};{host};;;;CONFAILURE"
                fh.write(logentry)
                msg = f"{host} no lookup possible, SSH connection failed"
                notify_syslog(msg)
                notify_im(msg)
            elif parameters == 'K22':
                logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};DFAILURE"
                fh.write(logentry)
                msg = f"{host} no Lookup possible, Datastore is missing or not accessible"
                notify_syslog(msg)
                notify_im(msg)
            elif parameters is None:
                logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};UNKNOWN"
                fh.write(logentry)
                msg = f"{host} Serial {facts['serial_number']} not assigned in Datastore"
                notify_syslog(msg)
                notify_im(msg)
            else:
                devicename = parameters['devicename']
                msg = f"{host} Serial {facts['serial_number']} assigned in Datastore -> Devicename: {devicename}"
                notify_syslog(msg)
                notify_im(msg)
                if os.path.isfile(C.CONFIG_DIR + devicename):
                    with open(os.path.join(C.CONFIG_DIR, devicename), "r") as fha:
                        logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};{devicename}"
                        config = fha.read()
                        fh.write(logentry)
                        fh.write(";!----BACKUP-CONFIGURATION:\n")
                        fh.write(config)
                        msg = f"{host} existing backup configuration for {devicename} found"
                        notify_syslog(msg)
                        notify_im(msg)
                else:
                    if parameters.get('ztp_template') is None or parameters.get('ztp_template') == '':
                        logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};DFAILURE"
                        fh.write(logentry)
                        msg = f"{host} no Rendering possible, Template not provided"
                        notify_syslog(msg)
                        notify_im(msg)
                    else:
                        config = render_file(parameters['ztp_template'], **parameters)
                        if config == 'T74':
                            logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};TFAILURE"
                            fh.write(logentry)
                            msg = f"{host} no Rendering possible, Template folder is missing or not accessible"
                            notify_syslog(msg)
                            notify_im(msg)
                        elif config == 'T68':
                            logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};TFAILURE"
                            fh.write(logentry)
                            msg = f"{host} no Rendering possible, Template {parameters['ztp_template']} not found"
                            notify_syslog(msg)
                            notify_im(msg)
                        elif config == 'T81':
                            logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};TFAILURE"
                            fh.write(logentry)
                            msg = f"{host} no Rendering possible, Template {parameters['ztp_template']} has undefined variables"
                            notify_syslog(msg)
                            notify_im(msg)
                        elif config == 'T82':
                            logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};TFAILURE"
                            fh.write(logentry)
                            msg = f"{host} no Rendering possible, Template {parameters['ztp_template']} has Syntax-Errors"
                            notify_syslog(msg)
                            notify_im(msg)
                        else:
                            logentry = f"{dtime};{host};{facts['hostname']};{facts['model']};{facts['serial_number']};{devicename}"
                            fh.write(logentry)
                            fh.write(";!----ZTP-CONFIGURATION:\n")
                            fh.write(config)
        os.chmod(C.CACHE_DIR + cachefile, 0o777)
    elif "ZTP" in file:
        ztpname = file.split('-')[0]
        cachefile = str(ztpname + ".log")
        timeout = 30
        i = 1
        while i != timeout and os.path.isfile(C.CACHE_DIR + cachefile) is False:
            time.sleep(1)
            i += 1
        if i == timeout:
            msg = f"{host} tasks timeout getting cache"
            notify_syslog(msg)
            return
        with open(os.path.join(C.CACHE_DIR, cachefile), "r") as fh:
            cache = fh.readline().split(';')
            devicename = cache[5]
            if devicename in ['CONFAILURE', 'DFAILURE', 'TFAILURE']:
                msg = f"{host} Provisioning failed, device will restart in 5 minutes"
                notify_syslog(msg)
                notify_im(msg)
                return
            elif devicename == 'UNKNOWN':
                msg = f"{host} Serial not assigned in datastore, please check and reset device manually"
                notify_syslog(msg)
                notify_im(msg)
                return

        time.sleep(15)

        dev = get_napalm_connection(host, 'ios')

        if dev:
            msg = f"{host} connection established"
            notify_syslog(msg)
        else:
            msg = f"{host} connection failed"
            notify_syslog(msg)
            return

        facts = dev.get_facts()
        if facts['hostname'] == devicename:
            msg = f"{host} {facts['hostname']} successfully provisioned, device will start embedded scripts in about 100s."
            notify_syslog(msg)
            notify_im(msg)
        else:
            msg = f"{host} something is wrong."
            notify_syslog(msg)
            notify_im(msg)

    dev.close()

