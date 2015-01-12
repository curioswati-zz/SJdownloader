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
Until now, it has individual python scripts for various tasks. The SJdownloader script in the downloader directory is the main script to run.  
It can be run from command-line by:  
	<code>python SJdownloader.py </code>  
Windows users first need to check their system's path variable set to contain the path to python.exe.  

Build from source:
------------------
Windows:
	Get the source from [here] (https://github.com/swati-jaiswal/SJdownloader/releases/download/v1.0.0/SJdownloader-1.0.0.zip)  
	After extracting the zip, from command line: 
	<code>
		cd /path/to/source  
		pyi-makespec --noconsole --icon=downloader/Icons/Logo.ico --onedir downloader/SJdownloader.py  
	</code>  
   	modify the generated spec file, add the following after the call to analyse:  
   	<code>
    	images = Tree('downloader/Icons', prefix='Icons')  
		configs = Tree('downloader/config', prefix='config')  
        </code>  
    next, in call to COLLECT, add the following on the second line, keep the indentation same:  
        <code>
    	[('README','README.txt','DATA')],  
        images,  
        configs,  
        </code>  
    run  
    <code>
    	pyinstaller SJdownloader.spec  
    </code>  
    you will find the exe in dist/SJdownloader/  
    
Dependencies:
-------------
wxpython:  
  [for windows] (http://www.wxpython.org/download.php#msw)  
  for linux:  
    <code>apt-get install wxpython</code>  
[pyinstaller] (https://pypi.python.org/pypi/PyInstaller/2.1)  
or else:  
<code>pip install pyinstaller</code>  

Standard modules used:
---------------------
* OS - It provides the script with some facilities of os, such as executing commands.  
       In the script, it is used for listing files in directories, and checking existence of directories.  
       For more information on OS, read the [documentation of OS][] .  

* wxpython - is a module used for creating GUIs in python.  
             [documentation of wxpython][]  

* urllib - provides a high level interface for fetching data across the world wide web.  
           For more information on OS, read the [documentation of urllib][]

Rest and required information is provided in the script itself.

[documentation of OS]: https://docs.python.org/2/library/os.html
[documentation of urllib]:https://docs.python.org/2/library/urllib.html
[documentation of wxpython]: http://wxpython.org/Phoenix/docs/html/main.html
[follow the link]: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/
[msvcp90.dll]: http://www.dll-files.com/dllindex/dll-files.shtml?msvcp90
[here]: https://github.com/swati-jaiswal/Downloader
