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
	
		:~$ sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n libwxgtk2.8-dev libgtk2.0-dev  

* [pyinstaller] (https://pypi.python.org/pypi/PyInstaller/2.1)  
  Or else:  

		:~$ pip install pyinstaller  

## Build from source:

### Windows:  
Get the source by:  
  1. Clone the repository.  

		:~$ git clone https://github.com/swati-jaiswal/SJdownloader.git  

You get a source directory named sjdownloader and some text files.  
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
Get the source by:  
        
        git clone https://github.com/swati-jaiswal/SJdownloader.git  

You get a source directory named sjdownloader and some text files.  
Now,  

    :~$ cd /path/to/source  
    :~$ pyi-makespec --noconsole --icon=sjdownloader/Icons/Logo.ico --onedir   

You will get a file named SJdownloader.spec in the current directory.  
Now modify the spec file, add the following after the call to Analyse, it should look like:  

        # -*- mode: python -*-  
        
        block_cipher = None  
        
        a = Analysis(['sjdownloader/SJdownloader.py'],  
                     pathex=['/home/dc-19/Desktop/sjdl'],  
                     hiddenimports=[],  
                     hookspath=None,  
                     runtime_hooks=None,  
                     excludes=None,  
                     cipher=block_cipher)  
        #----------------------------Add these lines here-----------------------------------
        images = Tree('sjdownloader/Icons', prefix='Icons')  
        configs = Tree('sjdownloader/config', prefix='config')  
        texts = [('README.txt','README.txt','DATA'), ('LICENSE.txt', 'LICENSE.txt', 'DATA')]  

Next, in call to COLLECT, add three following lines, it should look like:  

    coll = COLLECT(exe,
               texts,
               images,
               configs,  

After this you should run the following command from command prompt:  

    :~$ pyinstaller SJdownloader.spec  

you will find the executable SJdownloader in dist/SJdownloader/ under your current directory. You wil get a build/ directory also, it is better to remove that.
 
you can run it from terminal by typing:  
        
        :~$ ./SJdownloader

You can use the application in the above mentioned manner, but it will be better to configure it into your system path so that you are not bounded to use it inside any directory. Run the following commands:  

        :~$ sudo mkdir /usr/share/sjdownloader-1.0.0
        :~$ sudo cp dist/SJdownloader/Icons/sjdownloader-logo.png /usr/share/pixmaps/
        :~$ sudo mv dist/SJdownloader/* /usr/share/sjdownloader-1.0.0/
        :-$ echo "/usr/share/sjdownloader-1.0.0/SJdownloader" > sjdownloader
        :-$ chmod +x sjdownloader
        :-$ sudo mv sjdownloader /usr/bin/

Now you can run the application by command <code>sjdownloader</code>.
Create a file named sjdownloader.desktop and run the command:  

        sudo mv sjdownloader.desktop  /usr/share/applications/

Your application is now ready to be used.

External packages used:
----------------------
* [wxpython] (http://wxpython.org/Phoenix/docs/html/main.html).  

Rest and required information is provided in the script itself or you can visit the [wiki] (https://github.com/swati-jaiswal/SJdownloader/wiki/).
For updates visit the [project page] (http://swati-jaiswal.github.io/SJdownloader/).
