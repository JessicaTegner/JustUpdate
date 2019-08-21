## Utilities
Below are documentation on varius utilities found in JustUpdate.

## justupdate.repo.version.Version
The version class, can be used to validate version strings, get a human representation, compare too versions against each other and more.

~~~

from justupdate.repo.version import Version

test_version = Version("1.0.0a1")
test_version.to_human_readable() # 1.0.0 alpha 1
test_version.is_alpha() # True
test_version.is_beta() # False
test_version.is_stable() # False

other_version = Version("1.0.0a2")
test_version > other_version # False
test_version < other_version # True
test_version == other_version # False
~~~

