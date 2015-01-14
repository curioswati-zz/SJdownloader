#setup.py
from distutils.core import setup
import os

images = ['sjdownloader/Icons/'+file for file in os.listdir('sjdownloader/Icons')]
configs = ['sjdownloader/config/'+file for file in os.listdir('sjdownloader/config')]
License = ['LICENSE.txt']

setup(
	name='sjdownloader',
	version='1.0.0',
	description='Desktop application for internet content downloading.',
	long_description=open('README.txt').read(),
	license=open('LICENSE.txt').read(),
	author='Swati Jaiswal',
	author_email='jaiswalswati94@gmail.com',
	url='https://github.com/swati-jaiswal/SJdownloader',
	packages=['sjdownloader'],
	data_files=[('Icons', images),
                ('config', configs),
                ('LICENSE.txt', License)]
	)
