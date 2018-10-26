
# Purpose
Sunspec Alliance (https://sunspec.org/) is a trade alliance of more than 100 solar and storage distributed energy industry participants, together pursuing information standards to enable “plug & play” system interoperability. SunSpec standards address operational aspects of solar PV power and energy storage plants on the smart grid—including residential, commercial, and utility-scale systems—thus reducing cost, promoting technology innovation, and accelerating industry growth.

# How does it work
This application is written in Python, to query Sunspec compatible devices connected via Ethernet or RS485. This application will query 1 or more connected devices at regular intervals. Data will be written to log files on disk in a directory specified by the user. Usage and command line parameters are as follows:

## Install
On a raspberry Pi, or other Linux machines (arm, intel, mips or whetever), make sure Python is installed (which it should be). Then install the dependancies and this package as follows:
```
git clone --recursive https://github.com/sunspec/pysunspec.git
cd pysunspec
sudo python setup.py install
sudo pip install sunspec_ardexa
```

## Usage
To scan the whole (1-255) or part of the Sunspec address range and print out the device metadata, do the following
Note that the `port` default is `502` if not specified, and `baud` default is `115200` if not specified. Here are is the usage and some examples:
```
Usage: sunspec_ardexa discover IP_address/Device_Node Bus_Addresses
Example 1: sunspec_ardexa discover 192.168.1.3 1-5
Example 2: sunspec_ardexa discover 192.168.1.3 1,3-5 --port=502
Example 3: sunspec_ardexa discover /dev/ttyUSB0 1,3,5 --baud 115200
Example 4: sunspec_ardexa discover /dev/ttyUSB0 1
```

To send production data to a file on disk 
```
Usage: sunspec_ardexa log IP_address/Device_Node Bus_Addresses Output_directory
Example 1: sunspec_ardexa log 192.168.1.3 1-5 /opt/ardexa
Example 2: sunspec_ardexa log 192.168.1.3 1,3-5 /opt/ardexa --port=502
Example 3: sunspec_ardexa log /dev/ttyUSB0 1,3,5 /opt/ardexa --baud 115200
Example 4: sunspec_ardexa log /dev/ttyUSB0 1 /opt/ardexa
```

- IP_address/Device_Node = ..something like: `192.168.1.4` or `/dev/ttyUSB0`
- Bus_Addresses = List of bus addresses using commas and hyphens, e.g. `1-4,6,10-20` (this is an RS485 address, NOT Ethernet). 
- Output_directory = logging directory; eg; /opt/ardexa. The data will be written to subdirectories, and the latest data is stored in a `latest.csv`. All data is kept for historical purposes. 
- To view debug output, increase the verbosity using the `-v` flag. Standard (no messages, except errors), `-v` (discovery messages) or `-vv` (all messages)

## Sunspec devices
In this project, please take a look at the 'docs' directory. This is a document from Sunspec that details their specification (not subject to change). Ardexa currently collecs `inverter` and `storage` types. However the `discover` will show all devices.

## Inverter Types:
- Delta Inverters use 19200 baud by default
- Solaredge Inverters use 115200 baud by default

## Collecting to the Ardexa cloud
Collecting to the Ardexa cloud is free for up to 3 Raspberry Pis (or equivalent). Ardexa provides free agents for ARM, Intel x86 and MIPS based processors. To collect the data to the Ardexa cloud do the following:
- Create a `RUN` scenario to schedule the Ardexa Sunspec script to run at regular intervals (say every 300 seconds/5 minutes).
- Then use a `CAPTURE` scenario to collect the csv (comma separated) data from the filename `latest.csv` in `/opt/ardexa/...`. 
- The `Docs` directory contains a sample of the mapping and Ardexa yaml file.

## Help
Contact Ardexa at support@ardexa.com, and we'll do our best efforts to help.
