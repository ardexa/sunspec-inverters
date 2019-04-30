"""
To discover devices: sunspec_ardexa discover IP_address/Device_Node Bus_Addresses
Example 1: sunspec_ardexa discover 192.168.1.3 1-5
Example 2: sunspec_ardexa discover 192.168.1.3 1,3-5 --port=502
Example 3: sunspec_ardexa discover /dev/ttyUSB0 1,3,5 --baud 115200
Example 4: sunspec_ardexa discover /dev/ttyUSB0 1

To send production data to a file on disk: sunspec_ardexa log IP_address/Device_Node Bus_Addresses Output_directory
Example 1: sunspec_ardexa log 192.168.1.3 1-5 /opt/ardexa
Example 2: sunspec_ardexa log 192.168.1.3 1,3-5 /opt/ardexa --port=502
Example 3: sunspec_ardexa log /dev/ttyUSB0 1,3,5 /opt/ardexa --baud 115200
Example 4: sunspec_ardexa log /dev/ttyUSB0 1 /opt/ardexa

"""

# Copyright (c) 2018 Ardexa Pty Ltd
#
# This code is licensed under the MIT License (MIT).
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

from __future__ import print_function
import sys
import time
import os
import socket
import click
import ardexaplugin as ap
import sunspec.core.client as sp_client

PY3K = sys.version_info >= (3, 0)

PIDFILE = '/tmp/sunspec-ardexa-'
SINGLE_PHASE_INVERTER = 101
THREE_PHASE_INVERTER = 103
INVERTER_STRINGS = 160
STRING_COMBINER = 403
STORAGE = 124
TIMEOUT_VAL = 3.0
ATTEMPTS = 10

# This is the dictionary and list for a Single and Three Phase Inverter (101 and 103)
dict_inverter = {'A' : 'AC Current (A)', 'APHA' : 'AC Current 1 (A)', 'APHB' : 'AC Current 2 (A)', 'APHC' : 'AC Current 3 (A)',
                 'PPVPHAB' : 'AC Voltage 12 (A)', 'PPVPHBC' : 'AC Voltage 23 (A)', 'PPVPHCA' : 'AC Voltage 31 (A)',
                 'PHVPHA' : 'AC Voltage 1 (A)', 'PHVPHB' : 'AC Voltage 2 (A)', 'PHVPHC' : 'AC Voltage 3 (A)',
                 'W' : 'AC Power (W)', 'HZ' : 'Grid Freq (Hz)', 'PF' : 'Cos Phi', 'WH' : 'Total Energy (Wh)', 'DCA' : 'DC Current 1 (A)',
                 'DCV' : 'DC Voltage 1 (V)', 'DCW' : 'DC Power (W)', 'TMPCAB' : 'Cabinet Temperature (C)', 'TMPSNK' : 'Heat Sink Temperature (C)',
                 'TMPTRNS' : 'Transformer Temperature (C)', 'TMPOT' : 'Other Temperature (C)', 'ST' : 'Operating State',
                 'STVND' : 'Vendor Operating State', 'EVT1' : 'Event1'}
list_inverter = ['A', 'APHA', 'APHB', 'APHC', 'PPVPHAB', 'PPVPHBC', 'PPVPHCA', 'PHVPHA', 'PHVPHB', 'PHVPHC', 'W', 'HZ', 'PF', 'WH',
                 'DCA', 'DCV', 'DCW', 'TMPCAB', 'TMPSNK', 'TMPTRNS', 'TMPOT', 'ST', 'STVND', 'EVT1']

# This is the dictionary and list for a Storage (124)
dict_storage = {'WCHAMAX' : 'SetPt Max Charge (W)', 'STORCTL_MOD' : 'Storage Mode', 'CHASTATE' : 'State of Charge (%)',
                'INBATV' : 'Battery Voltage (V)', 'CHAST' : 'Charge Status', 'OUTWRTE' : 'Discharge Rate (%)', 'INWRTE' : 'Charge Rate (%)',
                'STROAVAL' : 'Available Energy (AH)'}
list_storage = ['WCHAMAX', 'STORCTL_MOD', 'CHASTATE', 'INBATV', 'CHAST', 'OUTWRTE', 'INWRTE', 'STROAVAL']

# This is the dictionary and list for a MPPT Inverter Extension (160)
dict_strings = {'Evt' : 'Global Events', 'N' : 'Number of Modules'}
list_strings = ['Evt', 'N']
dict_strings_repeating = {'ID' : 'Module ID', 'DCA' : 'DC Current (A)', 'DCV' : 'DC Voltage (V)', 'DCW' : 'DC Power (W)',
                          'TMP' : 'Temperature', 'DCST' : 'Operating State', 'DCEVT' : 'Module Events'}

# This is the dictionary and list for a String Combiner (403)
dict_combiner = {'Evt' : 'Global Events', 'N' : 'Number of Modules', 'DCA' : 'DC Current (A)', 'TMP' : 'Temperature'}
list_combiner = ['Evt', 'N', 'DCA', 'TMP']
dict_combiner_repeating = {'INID' : 'Module ID', 'INDCA' : 'DC Current (A)', 'INEVT' : 'Module Events'}


###~~~~~~~~~~~~~~~~~~~
dict_evt1 = {0 : 'Ground fault', 1 : 'DC over voltage', 2 : 'AC disconnect open', 3 : 'DC disconnect open', 4 : 'Grid disconnect',
             5 : 'Cabinet open', 6 : 'Manual shutdown', 7 : 'Over temperature', 8 : 'Frequency above limit', 9 : 'Frequency under limit',
             10 : 'AC Voltage above limit', 11 : 'AC Voltage under limit', 12 : 'Blown String fuse on input', 13 : 'Under temperature',
             14 : 'Generic Memory or Communication error (internal)', 15 : 'Hardware test failure'}

dict_storctl_mod = {0 : 'Charge', 1 : 'Discharge'}
dict_st = {1 : 'Off', 2 : 'Sleeping', 3 : 'Starting', 4 : 'MPPT', 5 : 'Throttled', 6 : 'Shutting down', 7 : 'Fault', 8 : 'Standby'}
dict_chast = {1 : 'Off', 2 : 'Empty', 3 : 'Discharging', 4 : 'Charging', 5 : 'Full', 6 : 'Holding', 7 : 'Testing'}
dict_evt = {0 : 'Ground Fault', 1 : 'Input Over Voltage', 19 : 'Reserved', 3 : 'DC Disconnect', 5 : 'Cabinet Open', 6 : 'Manual Shutdown', 7 : 'Over Temperature', 12 : 'Blown Fuse', 13 : 'Under Temperature', 14 : 'Memory Loss', 15 : 'Arc Detection', 20 : 'Test Failed', 21 : 'Under Voltage', 22 : 'Over Current'}
dict_dcst = {1 : 'Off', 2 : 'Sleeping', 3 : 'Starting', 4 : 'MPPT', 5 : 'Throttled', 6 : 'Shutting down', 7 : 'Fault', 8 : 'Standby',
             9 : 'Test', 19 : 'Reserved'}
dict_dcevt = {0 : 'Ground Fault', 1 : 'Input Over Voltage', 19 : 'Reserved', 3 : 'DC Disconnect', 5 : 'Cabinet Open', 6 : 'Manual Shutdown', 7 : 'Over Temperature', 12 : 'Blown Fuse', 13 : 'Under Temperature', 14 : 'Memory Loss', 15 : 'Arc Detection', 20 : 'Test Failed', 21 : 'Under Voltage', 22 : 'Over Current'}


def write_line(line, log_directory, header_line, debug):
    """This will write a line to the base_directory
    Assume header and lines are already \n terminated"""
    # Write the log entry, as a date entry in the log directory
    date_str = (time.strftime("%Y-%b-%d"))
    log_filename = date_str + ".csv"
    ap.write_log(log_directory, log_filename, header_line, line, debug, True, log_directory, "latest.csv")

    return True


def discover_devices(device_node, modbus_address, conn_type, baud, port, debug):
    try:
        if conn_type == 'tcp':
            port_int = int(port)
            sunspec_client = sp_client.SunSpecClientDevice(sp_client.TCP, modbus_address, ipaddr=device_node, ipport=port_int, timeout=TIMEOUT_VAL)
        elif conn_type == 'rtu':
            sunspec_client = sp_client.SunSpecClientDevice(sp_client.RTU, modbus_address, name=device_node, baudrate=baud, timeout=TIMEOUT_VAL)

        # read all models in the device
        sunspec_client.read()

    except:
        if debug > 0:
            print("Cannot find the address: ", modbus_address)
        return False

    print("Found a device at address: ", modbus_address)
    for model in sunspec_client.device.models_list:
        # Name may not exist
        try:
            if model.model_type.name:
                print("\nName: ", model.model_type.name, "\tSunspec Id: ", model.model_type.id, "\tLabel: ", model.model_type.label)
        except:
            pass

        for block in model.blocks:
            for point in block.points_list:
                if point.value is not None:
                    label = ""
                    suns_id = (point.point_type.id).strip().upper()
                    if point.point_type.label:
                        label = point.point_type.label
                    name = label + " (" + point.point_type.id + ")"
                    units = point.point_type.units
                    if not units:
                        units = ""
                    value = point.value
                    # Replace numbered status/events with description
                    value = convert_value(suns_id, value)
                    print('\t%-40s %20s %-10s' % (name, value, str(units)))

    return True


def extract_160_data(model, list_dev, dict_dev, debug):
    """This function will extract the data from a type 160 device
       It is different in that this type has a repeating block"""

    data_list = [""] * len(list_dev)
    header_list = list_dev[:]
    for idx, val in enumerate(header_list):
        if val in dict_dev:
            header_list[idx] = dict_dev[val]
        else:
            header_list[idx] = None

    if debug > 0:
        print("\nName: ", model.model_type.name, "\tSunspec Id: ", model.model_type.id, "\tLabel: ", model.model_type.label)
    for block in model.blocks:
        for point in block.points_list:
            suns_id = (point.point_type.id).strip().upper()
            # Check the value is present in the list we require
            if suns_id in dict_dev:
                value = ""
                if point.value is not None:
                    value = point.value
                # Replace numbered status/events with description
                value = convert_value(suns_id, value)

                # Put the data in the data_list
                index = list_dev.index(suns_id)
                data_list[index] = str(value)
                if debug > 0:
                    print('\t%-20s %20s' % (suns_id, value))

            # Else, if its in the repeating block, create a header AND data item
            elif suns_id in dict_strings_repeating:
                value = ""
                if point.value is not None:
                    value = point.value
                # Replace numbered status/events with description
                value = convert_value(suns_id, value)
                # ***Append*** to the data_list **AND** the header_list
                header_item = dict_strings_repeating[suns_id]
                header_list.append(header_item)
                data_list.append(str(value))
                if debug > 0:
                    print('\t%-20s %20s' % (suns_id, value))

    # Add a datetime and Log the line
    dt = ap.get_datetime_str()
    data_list.insert(0, dt)
    header_list.insert(0, 'Datetime')

    # Formulate the line
    line = ", ".join(data_list) + "\n"
    # And the header line
    header = "# " + ", ".join(header_list) + "\n"

    return header, line


def extract_403_data(model, list_dev, dict_dev, debug):
    """This function will extract the data from a type 403 device
       It is different in that this type has a repeating block"""

    data_list = [""] * len(list_dev)
    header_list = list_dev[:]
    for idx, val in enumerate(header_list):
        if val in dict_dev:
            header_list[idx] = dict_dev[val]
        else:
            header_list[idx] = None

    if debug > 0:
        print("\nName: ", model.model_type.name, "\tSunspec Id: ", model.model_type.id, "\tLabel: ", model.model_type.label)
    for block in model.blocks:
        for point in block.points_list:
            suns_id = (point.point_type.id).strip().upper()

            # Check the value is present in the list we require
            if suns_id in dict_dev:
                value = ""
                if point.value is not None:
                    value = point.value
                # Replace numbered status/events with description
                value = convert_value(suns_id, value)
                # Put the data in the data_list
                index = list_dev.index(suns_id)
                data_list[index] = str(value)
                if debug > 0:
                    print('\t%-20s %20s' % (suns_id, value))

            # Else, if its in the repeating block, create a header AND data item
            elif suns_id in dict_combiner_repeating:
                value = ""
                if point.value is not None:
                    value = point.value
                # Replace numbered status/events with description
                value = convert_value(suns_id, value)
                # ***Append*** to the data_list **AND** the header_list
                header_item = dict_combiner_repeating[suns_id]
                header_list.append(header_item)
                data_list.append(str(value))
                if debug > 0:
                    print('\t%-20s %20s' % (suns_id, value))

    # Add a datetime and Log the line
    dt = ap.get_datetime_str()
    data_list.insert(0, dt)
    header_list.insert(0, 'Datetime')

    # Formulate the line
    line = ", ".join(data_list) + "\n"
    # And the header line
    header = "# " + ", ".join(header_list) + "\n"

    return header, line


def extract_data(model, list_dev, dict_dev, debug):
    """This function will extract the data from a device"""

    data_list = [""] * len(list_dev)
    header_list = list_dev[:]
    for idx, val in enumerate(header_list):
        if val in dict_dev:
            header_list[idx] = dict_dev[val]
        else:
            header_list[idx] = None

    if debug > 0:
        print("\nName: ", model.model_type.name, "\tSunspec Id: ", model.model_type.id, "\tLabel: ", model.model_type.label)
    for block in model.blocks:
        for point in block.points_list:
            suns_id = (point.point_type.id).strip().upper()
            # Check the value is present in the list we require
            if suns_id in dict_dev:
                value = ""
                if point.value is not None:
                    value = point.value
                # Replace numbered status/events with description
                value = convert_value(suns_id, value)

                # Put the data in the data_list
                index = list_dev.index(suns_id)
                data_list[index] = str(value)
                if debug > 0:
                    print('\t%-20s %20s' % (suns_id, value))

    # Add a datetime and Log the line
    dt = ap.get_datetime_str()
    data_list.insert(0, dt)
    header_list.insert(0, 'Datetime')

    # Formulate the line
    line = ", ".join(data_list) + "\n"
    # And the header line
    header = "# " + ", ".join(header_list) + "\n"

    return header, line


def convert_value(name, value):
    """This will look up and replace numbers with descriptions"""

    if name == 'EVT1' and value in dict_evt1:
        value = dict_evt1[value]
    elif name == 'ST' and value in dict_st:
        value = dict_st[value]
    elif name == 'STORCTL_MOD' and value in dict_storctl_mod:
        value = dict_storctl_mod[value]
    elif name == 'CHAST' and value in dict_chast:
        value = dict_chast[value]
    elif name == 'EVT' and value in dict_evt:
        value = dict_evt[value]
    elif name == 'DCST' and value in dict_dcst:
        value = dict_dcst[value]
    elif name == 'DCEVT' and value in dict_dcevt:
        value = dict_dcevt[value]
    elif name == 'W':
        value = abs(value)

    return value


def log_devices(device_node, modbus_address, conn_type, baud, port, log_directory, debug):
    """This function writes a line of data based on Inverter 101, 103 or Storage 124"""

    try:
        if conn_type == 'tcp':
            port_int = int(port)
            sunspec_client = sp_client.SunSpecClientDevice(sp_client.TCP, modbus_address, ipaddr=device_node, ipport=port_int, timeout=TIMEOUT_VAL)
        elif conn_type == 'rtu':
            sunspec_client = sp_client.SunSpecClientDevice(sp_client.RTU, modbus_address, name=device_node, baudrate=baud, timeout=TIMEOUT_VAL)

        # read all models in the device
        sunspec_client.read()

    except:
        if debug > 0:
            print("Cannot find the address: ", modbus_address)
        return False

    for model in sunspec_client.device.models_list:
        full_log_directory = log_directory
        line = header = ""
        write = False

        # "id" may not exist
        try:
            # Log the data for an 101 (Single Phase) Inverter
            if model.model_type.id == SINGLE_PHASE_INVERTER or model.model_type.id == THREE_PHASE_INVERTER:
                header, line = extract_data(model, list_inverter, dict_inverter, debug)
                # Added "sunspec_101", device_node and modbus_address to the directory suffix
                full_log_directory = os.path.join(full_log_directory, "sunspec_101")
                write = True

            # Log the data for a device 124 (Storage)
            if model.model_type.id == STORAGE:
                header, line = extract_data(model, list_storage, dict_storage, debug)
                # Added "sunspec_124", device_node and modbus_address to the directory suffix
                full_log_directory = os.path.join(full_log_directory, "sunspec_124")
                write = True

            # Log the data for a device 160 (Strings)
            if model.model_type.id == INVERTER_STRINGS:
                header, line = extract_160_data(model, list_strings, dict_strings, debug)
                # Added "sunspec_160", device_node and modbus_address to the directory suffix
                full_log_directory = os.path.join(full_log_directory, "sunspec_160")
                write = True

            # Log the data for a device 403 (String Combiner)
            if model.model_type.id == STRING_COMBINER:
                header, line = extract_403_data(model, list_combiner, dict_combiner, debug)
                # Added "sunspec_403", device_node and modbus_address to the directory suffix
                full_log_directory = os.path.join(full_log_directory, "sunspec_403")
                write = True


            if write:
                # replace forward slashes
                devnode = device_node.replace("/", "_")
                full_log_directory = os.path.join(full_log_directory, str(devnode))
                full_log_directory = os.path.join(full_log_directory, str(modbus_address))
                if debug > 0:
                    print("Data line: ", line.strip())
                    print("Header line: ", header.strip())
                write_line(line, full_log_directory, header, debug)

        except:
            pass

    return True


class Config(object):
    """Config object for click"""
    def __init__(self):
        self.verbosity = 0


CONFIG = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('-v', '--verbose', count=True)
@CONFIG
def cli(config, verbose):
    """Command line entry point"""
    config.verbosity = verbose


@cli.command()
@click.argument('device')
@click.argument('modbus_addresses')
@click.option('--baud', default="115200")
@click.option('--port', default="502")
@CONFIG
def discover(config, device, modbus_addresses, baud, port):
    """Connect to the target IP address and run a scan of all Sunspec devices"""

    # Check that no other scripts are running
    # The pidfile is based on the device, since there are multiple scripts running
    pidfile = PIDFILE + device.replace('/', '-') + '.pid'
    if ap.check_pidfile(pidfile, config.verbosity):
        print("This script is already running")
        sys.exit(4)

    conn_type = 'tcp'
    try:
        socket.inet_aton(device)
    except socket.error:
        conn_type = 'rtu'

    start_time = time.time()

    # This will check each address
    for address in ap.parse_address_list(modbus_addresses):
        count = 0
        while count < ATTEMPTS:
            retval = discover_devices(device, address, conn_type, baud, port, config.verbosity)
            if retval:
                break
            count += 1
            time.sleep(1)

    elapsed_time = time.time() - start_time
    if config.verbosity > 0:
        print("This request took: ", elapsed_time, " seconds.")

    # Remove the PID file
    if os.path.isfile(pidfile):
        os.unlink(pidfile)


@cli.command()
@click.argument('device')
@click.argument('modbus_addresses')
@click.argument('output_directory')
@click.option('--baud', default="115200")
@click.option('--port', default="502")
@CONFIG
def log(config, device, modbus_addresses, output_directory, baud, port):
    """Connect to the target IP address and log the inverter output for the given bus addresses"""

    # If the logging directory doesn't exist, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Check that no other scripts are running
    # The pidfile is based on the device, since there are multiple scripts running
    pidfile = PIDFILE + device.replace('/', '-') + '.pid'
    if ap.check_pidfile(pidfile, config.verbosity):
        print("This script is already running")
        sys.exit(4)

    conn_type = 'tcp'
    try:
        socket.inet_aton(device)
    except socket.error:
        conn_type = 'rtu'

    start_time = time.time()

    # This will check each address
    for address in ap.parse_address_list(modbus_addresses):
        count = 0
        while count < ATTEMPTS:
            retval = log_devices(device, address, conn_type, baud, port, output_directory, config.verbosity)
            if retval:
                break
            count += 1
            time.sleep(1)

    elapsed_time = time.time() - start_time
    if config.verbosity > 0:
        print("This request took: ", elapsed_time, " seconds.")

    # Remove the PID file
    if os.path.isfile(pidfile):
        os.unlink(pidfile)
