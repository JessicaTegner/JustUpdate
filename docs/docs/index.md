# Welcome to JustUpdate
JustUpdate is a simple updater system, written for python, that uses each platforms native methods to perform an application update.

## installation
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
See <usage-cli> or <usage-client>



## Terminology for the CLI:
| term | explanation |
| ----------- | ---------------------------------------- |
| Build | the new version of the application in the build phase |
| JustUpdate Repository (ju-repo) | The repository is where the configuration, current builds, new and archived updates are kept. |
| commit | A version of your application commited to the JustUpdate Repository |
| upload service | The service used to upload the commited updates |

