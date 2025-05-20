from app.templating import render_file
from app.inventory import parameter_lookup
from app import configuration as C
import os
import sys
import datetime
import time


SERIAL = ''


def template_test(dtime, SERIAL):
    parameters = parameter_lookup(SERIAL)
    if parameters == 'K22':
        msg = 'No Lookup possible, Datastore is missing or not accessible'
        print(msg)
    elif parameters is None:
        msg = 'Serial {} not assigned in Datastore'.format(SERIAL)
        print(msg)
    else:
        ztplog = str("templating-test_" + SERIAL + ".log")
        with open(os.path.join(C.CACHE_DIR, ztplog), "w") as fh:
            devicename = parameters['devicename']
            msg = 'Serial {} assigned in Datastore -> Devicename: {}'.format(SERIAL, devicename)
            print(msg)
            if os.path.isfile(C.CONFIG_DIR + devicename):
                with open(os.path.join(C.CONFIG_DIR, devicename), "r") as f:
                    msg = 'Existing backup configuration for {} found'.format(devicename)
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, devicename)
                    config = f.read()
                    fh.write(logentry)
                    fh.write(";!----BACKUP-CONFIGURATION:\n")
                    fh.write(config)
            else:
                config = render_file(parameters['ztp_template'], **parameters)
                if config == 'T74':
                    msg = '{} no Rendering possible, Template folder is missing or not accessible'.format(SERIAL)
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, 'TFAILURE')
                    fh.write(logentry)
                elif config == 'T68':
                    msg = '{} no Rendering possible, Template {} is missing'.format(SERIAL, parameters['ztp_template'])
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, 'TFAILURE')
                    fh.write(logentry)
                elif config == 'T81':
                    msg = '{} no Rendering possible, Template {} includes not defined variables'.format(SERIAL, parameters['ztp_template'])
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, 'TFAILURE')
                    fh.write(logentry)
                elif config == 'T82':
                    msg = '{} no Rendering possible, Template {} has errors in Syntax'.format(SERIAL, parameters['ztp_template'])
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, 'TFAILURE')
                    fh.write(logentry)
                else:
                    msg = 'Rendering Configuration for {} to logfile {}{}'.format(SERIAL, C.CACHE_DIR, ztplog)
                    print(msg)
                    logentry = '{};{};{};{};{};{}'.format(dtime, "NA", "NA", "NA", SERIAL, devicename)
                    fh.write(logentry)
                    fh.write(";!----ZTP-CONFIGURATION:\n")
                    fh.write(config)
        os.chmod(C.CACHE_DIR + ztplog, 0o777)


def main(SERIAL):
    dtime = datetime.datetime.now()
    template_test(dtime, SERIAL)


if __name__ == '__main__':
    while SERIAL == '':
        SERIAL = input('Please enter the serial number of the device (only upper-case letters): ').strip()
    main(SERIAL)
    print('DONE')
