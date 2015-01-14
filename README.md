SJdownloader is a python project created for downloading stuff from internet.
* * *

## Introduction:

The project is initiated to provide a simple but yet powerful tool to download content from internet easily. It is not for commercial use. It provides a GUI based interface, where the user needs to enter url of site.
All the links available on the page are listed as soon as the url is entered.
There is option available to filter links according to user requirement.
I hope, it will be of help to all.

## Instructions:

The project is under work.
Until now, it has individual python scripts for various tasks. The SJdownloader script in the downloader directory is the main script to run.  
It can be run from command-line by:  
	<code>python SJdownloader.py </code>  
Windows users first need to check their system's path variable set to contain the path to python.exe.  

## Dependencies:

* wxpython:  
  [for windows] (http://www.wxpython.org/download.php#msw)  
  for linux:  
  
	apt-get install python-wxgtk2.8  

* [pyinstaller] (https://pypi.python.org/pypi/PyInstaller/2.1)  
  Or else:  

	pip install pyinstaller  

## Build from source:

### Windows:  
Get the source by either of following ways:  
1. git clone https://github.com/swati-jaiswal/SJdownloader.git  
2. Download the source from [here] (https://github.com/swati-jaiswal/SJdownloader/releases/download/v1.0.0/SJdownloader-1.0.0.zip) and extract the archive.  

In both cases you get a source directory named sjdownloader and some text files.  
When you clone the repository, you get this readme and  when you download the zip, you get another readme.  
both will have this stuff to help you with build process.  
Let's start the process.  

	>cd /path/to/source
	>pyi-makespec --noconsole --icon=sjdownloader/Icons/Logo.ico --onedir sjdownloader/SJdownloader.py  
		
modify the generated SJdownloader.spec file, add the following after the call to Analyse, on next line:  

    images = Tree('sjdownloader/Icons', prefix='Icons')
    configs = Tree('sjdownloader/config', prefix='config')  
    texts = [('README.txt','README.txt','DATA'), ('LICENSE.txt', 'LICENSE.txt', 'DATA')]  
    
next, in call to COLLECT, add three following lines, it should look like:  

    coll = COLLECT(exe,
               texts,
               images,
               configs,  
               
now from command line, run:  

    pyinstaller SJdownloader.spec  
    
you will find the exe in dist/SJdownloader/ under your current directory.   
Then move the SJdownloader to C:\Program Files\  
After that you can use the application in your system.  
For more info visit [here] (https://github.com/swati-jaiswal/SJdownloader/wiki/Build-instructions).

### Linux:
Get the source by downloading from [here] (https://github.com/swati-jaiswal/SJdownloader/releases/download/v1.0.0/SJdownloader-1.0.0.tar.gz) and extract the archive.  
open command prompt, then follow the commands:  

	$cd /path/to/source  
	$dpkg --build SJdownloader/ sjdownloader-1.0.0.deb  
	$dpkg -i sjdownloader-1.0.0.deb  

Standard modules used:
---------------------
* [OS] (https://docs.python.org/2/library/os.html).  
* [urllib] (https://docs.python.org/2/library/urllib.html).  
* [wxpython] (http://wxpython.org/Phoenix/docs/html/main.html).  

Rest and required information is provided in the script itself or you can visit the [wiki] (https://github.com/swati-jaiswal/SJdownloader/wiki/).
For updates visit the [project page] (http://swati-jaiswal.github.io/SJdownloader/).
