# Welcome to JustUpdate
JustUpdate is a simple updater system, written for python, that uses each platforms native methods to perform an application update.

## installation
#### Os specific requirements:
* Python3.
* For windows: NSIS version 3x.
* For Mac: the productbuild command available (can be installed by running the command in the terminal, or by installing xCode developer tools).

#### The module itself
To install do the following
~~~

pip install justupdate

~~~

or install from the git repository.

~~~

git clone <https://github.com/NicklasMCHD/JustUpdate.git>
cd JustUpdate
python setup.py install

~~~

## Usage:
See [usage cli](usage-cli.md) and [usage client](usage-client.md)



## Terminology for the CLI:
| term | explanation |
| ----------- | ---------------------------------------- |
| Build | the new version of the application in the build phase |
| JustUpdate Repository (ju-repo) | The repository is where the configuration, current builds, new and archived updates are kept. |
| commit | A version of your application commited to the JustUpdate Repository |
| upload service | The service used to upload the commited updates |


## helping out
Have you found this utility helpful and wan't to support me in my work?
you are welcome to [buy me a coffee (isn't that what they all say... Or is it pizza, nevermind... You know what I mean.)](https://paypal.me/NicklasMCHD) or alternatively [follow me on twitter](https://twitter.com/NicklasMCHD)
