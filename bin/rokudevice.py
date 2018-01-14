import requests
import xml.etree.ElementTree as eT


class RokuDevice:
    keypress_values = ['Home', 'Rev', 'Fwd', 'Play', 'Select', 'Left', 'Right', 'Down', 'Up', 'Back',
                       'InstantReplay', 'Info', 'Backspace', 'Search', 'Enter', 'VolumeDown', 'VolumeMute', 'VolumeUp',
                       'PowerOff', 'ChannelUp', 'ChannelDown', 'InputTuner', 'InputHDMI1', 'InputHDMI2', 'InputHDMI3',
                       'InputHDMI4', 'InputAV1']

    def __init__(self):
        self.apps = {}
        self.ip_address = ''
        self.device_name = ''
        self.current_app_name = ''

    def get_device_info(self):
        response = requests.get(url=self.ip_address + '/query/device-info')
        self.device_name = self.parse_device_info(response.text)

    @staticmethod
    def parse_device_info(xml):
        tree_root = eT.fromstring(xml)
        user_defined_name = tree_root.find('user-device-name').text
        return user_defined_name

    def get_current_app(self):
        response = requests.get(url=self.ip_address + '/query/active-app')
        root = eT.fromstring(response.text)
        self.current_app_name = root.find('app').text

    def get_apps(self):
        response = requests.get(url=self.ip_address + '/query/apps')
        root = eT.fromstring(response.text.encode('utf-8').strip())
        for app in root.findall('app'):
            self.apps[app.text] = app.attrib['id']

    def send_command(self, command):

        if command.lower() == 'apps':
            for key in self.apps.keys():
                print('\t' + key)
            return True

        if command.lower() == 'change device':
            return False

        if command.lower() in (app_name.lower() for app_name in self.apps.keys()):
            command = '/launch/' + self.apps[command]

        if command.lower() in (name.lower() for name in self.keypress_values):
            command = '/keypress/' + command

        requests.post(url=self.ip_address + command)
        return True
