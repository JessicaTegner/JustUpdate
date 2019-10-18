from setuptools import find_packages, setup

import versioneer

KEYWORDS = (
    "PyUpdater Pyinstaller Auto Update AutoUpdate Auto-Update Esky simple updater mac/updater windows/updater "
    "updater4pyi bbfreeze ccfreeze freeze cz_freeze pyupdate"
)


with open(u"requirements.txt", u"r") as f:
    required = f.read().splitlines()


with open("README.md", "r") as f:
    readme = f.read()


setup(
    name="JustUpdate",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Tired of complex updaters that doesn't work. Use JustUpdate, that uses os native solutions to perform the update.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="NicklasMCHD",
    url="https://github.com/NicklasMCHD/JustUpdate",
    license="GNU LGPLv3",
    keywords=KEYWORDS,
    zip_safe=False,
    include_package_data=True,
    tests_require=["pytest"],
    install_requires=required,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    justupdate=justupdate.cli:main
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Topic :: Software Development :: Build Tools",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
