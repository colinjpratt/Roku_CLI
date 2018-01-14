#!/usr/bin/env python

import sys
import ssdp
from rokudevice import RokuDevice


def main():

    print('Finding Devices....')
    # Discover Roku Devices
    all_devices = ssdp.discover('roku:ecp')
    # Get the device info for each roku
    # Display the user named device as a list to chose from
    # Accept user input for device commands 
    selected_device = select_device(all_devices)
    wait_for_command(selected_device)


def select_device(device_list):

    devices = []
    for value in device_list:
        # print(value.location)
        new_device = RokuDevice()
        new_device.ip_address = value.location
        new_device.get_device_info()
        devices.append(new_device)

    # if only on device skip
    if len(devices) == 1:
        current_device = devices[0]
    else:
        while 1:
            print('\rChoose a device to control:')
            for idx, device in enumerate(devices):
                print('\t ' + str(idx + 1) + '.' + device.device_name)
            selected_device_index = int(raw_input(''))
            if selected_device_index <= len(devices):
                current_device = devices[selected_device_index - 1]
                break
            else:
                print('Invalid Selection')

    print(current_device.device_name.title() + ":" + current_device.ip_address + ' Selected')
    return current_device


def wait_for_command(device):

    device.get_apps()

    print('Send Command to Device...')
    while 1:
        device.get_current_app()
        new_command = raw_input(device.device_name + ' - ' + device.current_app_name + ': ')
        more = device.send_command(new_command)
        if not more:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
