#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()
import setuptools, glob

data = [('share/chirp/glade',  glob.glob('glade/*.glade')),
        ('share/applications' , ['chirp.desktop']),
        ('share/pixmaps' , ['chirp.png'])]

setuptools.setup (
	name='chirp',
	version='0.1',
        scripts=['scripts/chirp'],
        packages=['chirp'],
        package_dir={'chirp': 'src'},
        data=data,
        ext_package='chirp',
	author='George Pomortsev',
	author_email='illicium@gmail.com',
	description='Twitter desktop client',
	long_description='Python/GTK+ Twitter desktop client',
	license='New BSD License',
	url='http://code.google.com/p/chirp',
	keywords='twitter desktop client gtk python',
	install_requires = ['python-twitter >= 0.2']
)
