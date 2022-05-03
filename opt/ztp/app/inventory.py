from app import configuration as C
import csv
import os

def parameter_lookup (serial):

    config_parameters = []
    if not os.path.isfile(C.KEYSTORE):
        return('K22')
    else:
        with open(C.KEYSTORE) as fh:
            csv_reader = csv.DictReader(fh, delimiter=';')
            for line in csv_reader:
                config_parameters.append(dict(line))

        for entry in config_parameters:
            idarray = []
            for i in range(1, 9):
                idarray_entry = entry['idarray_{}'.format(i)]
                if (idarray_entry != '') and (idarray_entry != None):
                    idarray.append(idarray_entry)
            entry['idarray'] = idarray

        for parameter in config_parameters:
            if serial in parameter['idarray']:
                config_parameters = []
                config_parameters.append(parameter)
                return(config_parameters)

