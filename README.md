# nautilus-pushbullet
A Nautilus extension to push files via http://www.pushbullet.com. Pushing files to individual devices, contacts and channels is supported.

Dependencies:
* nautilus
* nautilus-python
* python2-pushbullet (https://pypi.python.org/pypi/pushbullet.py)

Installation:
 * sudo mkdir -p /usr/share/nautilus-python/extensions
 * sudo install -m755 nautilus-pushbullet.py /usr/share/nautilus-python/extensions/nautilus-pushbullet.py
 * sudo ln -s /usr/share/nautilus-python/extensions/nautilus-pushbullet.py /usr/bin/nautilus-pushbullet
 * nautilus-pushbullet

The last commands propts you to enter you Access Token (API) and the current device name of pushbullet (e.g. the name of your Browser).
Entering the current device name makes sure that you do not push files to yourself.
You only need to run the last command once.
 
