#setup.py
from distutils.core import setup

setup(
	name='SJDownloader',
	version='1.0.0',
	description='Desktop application for internet content downloading.',
	long_description=open('README.md').read(),
	author='Swati Jaiswal',
	author_email='jaiswalswati94@gmail.com',
	url='https://github.com/swati-jaiswal/Downloader',
	packages=['downloader'],
	data_files=[('Icons', ['Icons/folder.png','Icons/Logo.png','Icons/new.png','Icons/package.png','Icons/pref.png']),
                ('config', ['config/config.txt','config/content.txt'])],
	)
