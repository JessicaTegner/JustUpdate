# Usage CLI

The cli (command line interface) is one of two essential parts of JustUpdate.
The CLI is what's will be helping you producing, commiting and uploading your update packages.

## Initialization
First up, initialize a JustUpdate repository.

~~~

	justupdate init

~~~

go through the onscreen prompts to finish the initialization.

## Creating a spec file.
Note: You'll need to do this on each platform you want to produce builds for.

If you haven't already, you'll need to generate a JustUpdate spec file.

~~~

justupdate make-spec pyinstaller_arguments scriptfile

~~~

* replace "pyinstaller_arguments" with actual PyInstaller arguments.
Note: At this moment in time, **--onedir** and **--windowed** are required on MacOS, because JustUpdate only work with MacOS Application Bundles.


## Producing a build
Note: You'll need to do this on each platform, you want to produce a build for.
After generating a spec file, run the folowing command to produce a build.

~~~

justupdate build spec-file

~~~

## Commiting a new version
Note: You'll need to do this on each platform, after generating a build for that platform

When you have asured that your build works as expected, you can commit it to the history in the JustUpdate repository like so.

~~~

justupdate commit version

~~~

#### Valid versions
Versions are deemed valid if the following criteria are met.

* At least 3 numbers separated by dots.
* (optional) the letter indicating if it's an alpha (a) or beta (b) followed by a number indicating which alpha/beta number it is.

Below are some examples for some valid version numbers.

* 1.2.3 (a stable version)
* 1.4.5a12 (An alpha)
* 2.0.0b7 (A beta version)


## Upload all the commited versions
After generating builds and commiting them for the wanted platforms, it's time to upload them.
This only needs to be done once and can be done the following way.

To get information about the available uploader services, run the following command.

~~~

justupdate upload

~~~

After finding a service to your liking, run the following command with the service name from the above list, to initate the update.

~~~

justupdate upload -s service

~~~

If it's the first time uploading with this service in the JustUpdate repository, the initialization for that service will start.
The scp, as an example, will begin to ask you for connection information and remote path to store the JustUpdate files.
The uploader service initialization is a one time process and will be remembered for later use (only in that JustUpdate repository).
Note: The credentials for each initialized uploader service will be saved to **"ju-repo/credentials.dat"**




