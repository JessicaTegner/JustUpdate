# Templates
These templates are used, on each platform, to provide the self-installation part of the update process.

### Variable descriptions.
In all the templates, a group of variables are available.
Each variable will be replaced with their corresponding value.
Each variable name is incloded in a set of "%". So a variable will look like "%VARIABLE_NAME_HERE%". Each variable name is uppercased.

Variable name - variable replacement
APP_NAME - The apps name set on initalization
APP_AUTHOR - The apps author set on initalization
VERSION - The version of the app being created, as is (including channels)
COMPLIANT_VERSION - The version of the app being created, changed to be compliant with each platforms version requirements.
JustUpdateRepository - the path to the Just Update repository folder ("ju-repo" by default).
