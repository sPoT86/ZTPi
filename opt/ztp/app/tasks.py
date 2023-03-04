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
    if file == 'network-confg':
        dtime = datetime.datetime.now()
        msg = '{} downloaded {}'.format(host, file)
        notify_syslog('{}: {}'.format(dtime, msg))
        notify_im(msg)

        dev = get_napalm_connection(host, 'ios')

        if dev:
            msg = '{} connection established'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
        else:
            msg = '{} connection failed, giving up'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
            return

        facts = dev.get_facts()
        msg = '{} {}/{}/{}'.format(host, facts['hostname'], facts['model'], facts['serial_number'])
        notify_syslog('{}: {}'.format(dtime, msg))
        notify_im(msg)
        cachefile = str(facts['hostname'] + ".log")
        parameters = parameter_lookup(facts['serial_number'])
        with open(os.path.join(C.CACHE_DIR, cachefile), "w") as fh:
            if parameters == 'K22':
                msg = '{} no Lookup possible, Datastore is missing or not accessible'.format(host)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'DFAILURE')
                fh.write(logentry)
            elif parameters is None:
                msg = '{} Serial {} not assigned in Datastore'.format(host, facts['serial_number'])
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'UNKNOWN')
                fh.write(logentry)
            else:
                devicename = parameters['devicename']
                msg = '{} Serial {} assigned in Datastore -> Devicename: {}'.format(host, facts['serial_number'], devicename)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                if os.path.isfile(C.CONFIG_DIR + devicename):
                    with open(os.path.join(C.CONFIG_DIR, devicename), "r") as f:
                        msg = '{} existing backup configuration for {} found'.format(host, devicename)
                        notify_syslog('{}: {}'.format(dtime, msg))
                        notify_im(msg)
                        logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], devicename)
                        config = f.read()
                        fh.write(logentry)
                        fh.write(";!----BACKUP-CONFIGURATION:\n")
                        fh.write(config)
                else:
                    if parameters.get('ztp_template') is None or parameters.get('ztp_template') == '':
                        logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'DFAILURE')
                        fh.write(logentry)
                        msg = '{} no Rendering possible, Template not provided'.format(host)
                        notify_syslog('{}: {}'.format(dtime, msg))
                        notify_im(msg)
                    else:
                        config = render_file(parameters['ztp_template'], **parameters)
                        if config == 'T74':
                            logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'TFAILURE')
                            fh.write(logentry)
                            msg = '{} no Rendering possible, Template folder is missing or not accessible'.format(host)
                            notify_syslog('{}: {}'.format(dtime, msg))
                            notify_im(msg)
                        elif config == 'T68':
                            logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'TFAILURE')
                            fh.write(logentry)
                            msg = '{} no Rendering possible, Template {} not found'.format(host, parameters['ztp_template'])
                            notify_syslog('{}: {}'.format(dtime, msg))
                            notify_im(msg)
                        elif config == 'T81':
                            logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'TFAILURE')
                            fh.write(logentry)
                            msg = '{} no Rendering possible, Template {} has not defined variables'.format(host, parameters['ztp_template'])
                            notify_syslog('{}: {}'.format(dtime, msg))
                            notify_im(msg)
                        elif config == 'T82':
                            logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], 'TFAILURE')
                            fh.write(logentry)
                            msg = '{} no Rendering possible, Template {} has Syntax-Errors'.format(host, parameters['ztp_template'])
                            notify_syslog('{}: {}'.format(dtime, msg))
                            notify_im(msg)
                        else:
                            logentry = '{};{};{};{};{};{}'.format(dtime, host, facts['hostname'], facts['model'], facts['serial_number'], devicename)
                            fh.write(logentry)
                            fh.write(";!----ZTP-CONFIGURATION:\n")
                            fh.write(config)
        os.chmod(C.CACHE_DIR + cachefile, 0o777)
    elif "ZTP" in file:
        dtime = datetime.datetime.now()
        msg = '{} downloaded {}'.format(host, file)
        notify_syslog('{}: {}'.format(dtime, msg))
        notify_im(msg)
        ztpname = file.split('-')[0]
        cachefile = str(ztpname + ".log")
        timeout = 10
        i = 1
        while i != timeout and os.path.isfile(C.CACHE_DIR + cachefile) is False:
            time.sleep(1)
            i += 1
        if i == timeout:
            msg = '{} Provisioning failed, device will restart in 5 minutes'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
            return
        with open(os.path.join(C.CACHE_DIR, cachefile), "r") as f:
            cache = f.readline().split(';')
            if len(cache) < 6:
                msg = '{} Provisioning failed, device will restart in 5 minutes'.format(host)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                return
            devicename = cache[5]
            if devicename == 'DFAILURE':
                msg = '{} Provisioning failed, device will restart in 5 minutes'.format(host)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                return
            elif devicename == 'TFAILURE':
                msg = '{} Provisioning failed, device will restart in 5 minutes'.format(host)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                return
            elif devicename == 'UNKNOWN':
                msg = '{} Serial not assigned in datastore, please check datastore entry and reset device manually'.format(host)
                notify_syslog('{}: {}'.format(dtime, msg))
                notify_im(msg)
                return

        time.sleep(15)

        dev = get_napalm_connection(host, 'ios')

        if dev:
            msg = '{} connection established'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
        else:
            msg = '{} connection failed, giving up'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
            return

        facts = dev.get_facts()
        if facts['hostname'] == devicename:
            msg = '{} {} successfully provisioned, device will start embedded scripts in about 100s.'.format(host, facts['hostname'])
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)
        else:
            msg = '{} something is wrong, the result is not as it should be.'.format(host)
            notify_syslog('{}: {}'.format(dtime, msg))
            notify_im(msg)

    dev.close()

