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

        super(test, self).__init__(api_key = self.api_key)

        if self.user_info == {}:
            Notify.init('pushbullet-nautilus')
            n = Notify.Notification.new('Pushbullet-Nautilus not correctly configured', 'Please run ''nautilus-pushbullet'' in a Terminal to reconfigure', "dialog-information")
            n.show()
            Notify.uninit()

    # Push files to specified devices
    def push(self, menu, files, devices=[], contacts=[], channels=[]):

        for f in files:
            p = urlparse.urlparse(f.get_uri())
            finalPath = os.path.abspath(os.path.join(p.netloc, p.path))

            with open(finalPath, "rb") as tmp:
                success, file_data = self.upload_file(tmp, os.path.basename(finalPath))
                if success:
                    for device in devices:
                        success, push = self.push_file(device=device, **file_data)
                    for contact in contacts:
                        success, push = self.push_file(contact=contact, **file_data)
                    for channel in channels:
                        success, push = self.push_file(channel=channel, **file_data)

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
                                         label='Pushbullet',
                                         tip='',
                                         icon='')


        submenu_dev = Nautilus.Menu()
        top_menuitem.set_submenu(submenu_dev)

        if self.devices == []:
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::None',
                                             label='No devices, check configuration',
                                             tip='',
                                             icon='')
            submenu_dev.append_item(sub_menuitem)
        else:
            # Menu entry for sending to all devices
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::All',
                                             label='All Devices',
                                             tip='',
                                             icon='')

            sub_menuitem.connect('activate', self.push, files, self.devices)
            submenu_dev.append_item(sub_menuitem)

        # Menu entries for sending to individual devices
        for device in devices:

            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::'+device.nickname,
                                             label=device.nickname,
                                             tip='',
                                             icon='')

            sub_menuitem.connect('activate', self.push, files, [device])
            submenu_dev.append_item(sub_menuitem)

        # Contacts submenu entry
        if len(self.contacts) > 0:
            submenu_con = Nautilus.Menu()
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::Contacts',
                                             label='Contacts',
                                             tip='',
                                             icon='')

            sub_menuitem.set_submenu(submenu_con)
            submenu_dev.append_item(sub_menuitem)

            for contact in self.contacts:
                if not contact.active:
                    continue
                sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::Contacts'+contact.name,
                                                    label=contact.name,
                                                    tip='',
                                                    icon='')
                sub_menuitem.connect('activate', self.push, files, [], [contact])
                submenu_con.append_item(sub_menuitem)

        # Channels submenu entry
        if len(self.channels) > 0:
            submenu_con = Nautilus.Menu()
            sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::Channels',
                                             label='Channels',
                                             tip='',
                                             icon='')

            sub_menuitem.set_submenu(submenu_con)
            submenu_dev.append_item(sub_menuitem)

            for channel in self.channels:
                if not contact.active:
                    continue
                sub_menuitem = Nautilus.MenuItem(name='NautilusPushbullet::Push::Contacts'+channel.name,
                                                    label=channel.name,
                                                    tip='',
                                                    icon='')
                sub_menuitem.connect('activate', self.push, files, [], [], [channel])
                submenu_con.append_item(sub_menuitem)

        return top_menuitem,


    def get_background_items(self, window, file):
        return None


if __name__ == '__main__':
    api_key = raw_input('Please enter your Pushbullet Access Token: ')
    excluded = raw_input('Please enter the name of your current device (optional): ')
    write_config(api_key, excluded)
