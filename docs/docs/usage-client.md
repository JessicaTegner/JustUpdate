# Usage Client

The client is the python module that your application will import to check, download and execute updates created through the cli interface.


## Initialization

First up, you'll need to import the JustUpdateClient, the ClientConfig you generated when setting up the cli, and any other modules you may need.

~~~

from justupdate.client.client import JustUpdate
from client_config import ClientConfig

~~~

Then instantiate a JustUpdateClient object, passing in the required parameters

~~~

client = JustUpdateClient(ClientConfig(), "1.0.0", "stable")

~~~

You can also set a callback directly in the JustUpdateClient constructor, like so:

~~~

client = JustUpdateClient(ClientConfig(), "1.0.0", "stable", update_callback)

~~~

* The first parameter is an instance to the client config you generated before.
* The second parameter is the current version of your application.
* the third parameter is the release channel you wan't to listen for updates on.
* The fourth parameter, which is optional, is a callable, that takes one parameter, that will be used as callbacks later.

You can also set a callback later (useful if you wan't different things to happen depending on other factors)

~~~

client.add_callback(update_callback)

~~~

Note: There's no limit to how many callbacks you can attach.


## Checking for updates

Then after initializing the JustUpdateClient, you can perform an update check with the following

~~~

if client.update_available():
    # proceed to download.
else:
    # no update available, we are up to date.

~~~

## Downloading the update.

After checking for updates, if an update is available, you can download it one of too ways, Asynchronous or Synchronous.
The **background** flag in the download_update function, is used to tell, if you wan't to download Asynchronous or Synchronous.

#### Downloading the update Synchronously

If you choose to download the update Synchronously, the download_update function will return when the update package has been downloaded and are ready to be executed.

~~~

client.download_update(background=False)

~~~


#### Downloading the update asynchronously

If you choose to download the update asynchronously, the download_update function will return immediately, so you'll get a chance to keep the ui in your application responsive, show a progress bar or whatever you may like to do, while the update is downloading.

~~~

client.download_update(background=True)
while client.is_downloaded() == False:
	pass # do nothing, the percentage and other properties of the download are sent to the callbacks you have registered.

~~~


## Executing the update

After downloading the update package, you can execute the update like so.
Important: Your application should quit right after running the execute_update function, any saving or cleanup on your end, should be called before calling the execute_update function.

~~~

client.execute_update()
sys.exit(0)

~~~


## Post update actions

It's possible to do something after an update has been performed (the first time your application starts after an update).
To start, you'll need to initialize the JustUpdateClient object again, before you'll be able to check to see, if this is a post update situation.

~~~

client = ... # JustUpdateClient initialization, same as above
if client.is_post_update():
    # do some post update actions, like displaying a changelog.

~~~

When you're done with your post update actions, you need to tell JustUpdate, that it can clean up it's post update reference (so your post update actions doesn't trigger later, by mistake).

~~~

client.post_update_cleanup()

~~~

