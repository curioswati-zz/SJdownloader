Downloader is a python project created for downloading stuff from internet.
* * *

Introduction:
------------
The project is initiated to provide a simple but yet powerful tool to download content from internet easily. It is not for commercial use. It provides a GUI based interface, where the user needs to enter url of site.
All the links available on the page are listed as soon as the url is entered.
There is option available to filter links according to user requirement.
I hope, it will be of help to all.

Instructions:
------------
The project is under work.
Until now, it has individual python scripts for various tasks, which are all written here only. The GUI script is the main script to run.

Dependencies:
-------------
All the dependencies are mentioned in the requirement file.
For py2exe listed in requirements file, python 3 is required. For python 2 [follow the link][].
For py2exe, you may require [msvcp90.dll][].

Standard modules used:
---------------------
OS, urllib module and wxpython are used.
It provides the script with some facilities of os, such as executing commands.
In the script, it is used for listing files in directories, and checking existence of directories.
For more information on OS, read the [documentation of OS][] .

wxpython is a module used for creating GUIs in python.
[documentation of wxpython][]

urllib provides a high level interface for fetching data across the world wide web.
For more information on OS, read the [documentation of urllib][]

Rest and required information is provided in the script itself.

[documentation of OS]: https://docs.python.org/2/library/os.html
[documentation of urllib]:https://docs.python.org/2/library/urllib.html
[documentation of wxpython]: http://wxpython.org/Phoenix/docs/html/main.html
[follow the link]: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/
[msvcp90.dll]: http://www.dll-files.com/dllindex/dll-files.shtml?msvcp90
