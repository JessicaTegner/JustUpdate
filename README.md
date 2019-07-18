# Just. Fucking. Update
Just. Fucking. Update, is a updater system, written in python, that utilizes each platforms native method of installing an application, to perform an update.
* On windows, JFU uses NSIS (nullsoft scriptable install system) to perform the update.
* On Mac, JFU uses the pkg mechanics to perform the update.

### Requirements.
* Python3.
* pip install -r requirements.txt
* For windows: NSIS version 3x.
* For Mac: the pkgbuild command available (can be installed by running the command in the terminal, or by installing xCode developer tools).
