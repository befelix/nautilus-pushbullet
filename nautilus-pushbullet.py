#! /usr/bin/env python2

from pushbullet import PushBullet
from gi.repository import Nautilus, GObject, Notify

import urlparse
import os.path

import ConfigParser

CONFIG_FILE = os.path.expanduser('~/.config/nautilus-pushbullet.conf')

def read_config():
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)

    api  = config.get('User Data', 'access_token')
    excl = config.get('User Data', 'excluded_device')

    return api,excl

def write_config(api, exclude=''):

    config = ConfigParser.RawConfigParser()
    config.add_section('User Data')
    config.set('User Data', 'access_token', api)
    config.set('User Data', 'excluded_device', exclude)

    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)



class test(PushBullet, GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        self.api_key, self.exclude = read_config()
        #self.exclude = 'Firefox'
        #self.api_key = 'eEd1WXVecVkAa1rmvZRdiY0iBdisHMlI'
        super(test, self).__init__(api_key = self.api_key)

        if self.user_info == {}:
            Notify.init('pushbullet-nautilus')
            n = Notify.Notification.new('Pushbullet-Nautilus not correctly configured', 'Please run ''nautilus-pushbullet'' in a Terminal to reconfigure', "dialog-information")
            n.show()
            Notify.uninit()





    # Push files to specified devices
    def push(self, menu, files, devices):

        for f in files:
            p = urlparse.urlparse(f.get_uri())
            finalPath = os.path.abspath(os.path.join(p.netloc, p.path))

            with open(finalPath, "rb") as tmp:
                success, file_data = self.upload_file(tmp, os.path.basename(finalPath))
                if success:
                    for device in devices:
                        success, push = self.push_file(device=device, **file_data)

    # Alter Nautilus menu items
    def get_file_items(self, window, files):

        # Skip for directories...pushing those files individually can lead to a huge mess
        for file in files:
            if file.is_directory():
                return None

        # all devices that can be pushed to and are not excluded
        devices = [device for device in self.devices if device.pushable and not device.nickname == self.exclude]

        # Top menu
        top_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push',
                                         label='Push to Pushbullet',
                                         tip='',
                                         icon='')

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        if self.devices == []:
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::None',
                                             label='No devices, check configuration',
                                             tip='',
                                             icon='')
            submenu.append_item(sub_menuitem)
        else:
            # Menu entry for sending to all devices
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::All',
                                             label='ALL',
                                             tip='',
                                             icon='')

            sub_menuitem.connect('activate', self.push, files, self.devices)
            submenu.append_item(sub_menuitem)

        # Menu entries for sending to individual devices
        for device in devices:

            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::'+device.nickname,
                                             label=device.nickname,
                                             tip='',
                                             icon='')

            sub_menuitem.connect('activate', self.push, files, [device])

            submenu.append_item(sub_menuitem)


        return top_menuitem,


    def get_background_items(self, window, file):
        return None


if __name__ == '__main__':
    api_key = raw_input('Please enter your Pushbullet Access Token: ')
    excluded = raw_input('Please enter the name of your current device (optional): ')
    write_config(api_key, excluded)
