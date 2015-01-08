#setup.py
from distutils.core import setup
import py2exe
import os

images = ['downloader/Icons/'+file for file in os.listdir('downloader/Icons')]
configs = ['downloader/config/'+file for file in os.listdir('downloader/config')]

setup(
	name='SJdownloader',
	version='1.0.0',
	description='Desktop application for internet content downloading.',
	license=open('LICENSE.txt').read()
	long_description=open('README.md').read(),
	author='Swati Jaiswal',
	author_email='jaiswalswati94@gmail.com',
	url='https://github.com/swati-jaiswal/Downloader',
	packages=['downloader'],
	data_files=[('Icons', images),
                ('config', configs)],
	)