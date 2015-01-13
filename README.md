# nautilus-pushbullet
A Nautilus extension to push files via http://www.pushbullet.com. Pushing files to individual devices, contacts and channels is supported.

Dependencies:
* nautilus
* python2-pushbullet (https://pypi.python.org/pypi/pushbullet.py)

Installation:
 * sudo mkdir -p /usr/share/nautilus-python/extensions
 * sudo install -m755 nautilus-pushbullet.py /usr/share/nautilus-python/extensions/nautilus-pushbullet.py
 * sudo ln -s /usr/share/nautilus-python/extensions/nautilus-pushbullet.py /usr/bin/nautilus-pushbullet
 * nautilus-pushbullet

The last commands propts you to enter you Access Token (API) and the current device name of pushbullet. The restricted device stops the script from pushing to the device you are currently working on. This command needs to be run only once.
 
