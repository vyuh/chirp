import ez_setup
ez_setup.use_setuptools()
import setuptools

data = [('share/applications' , ['chirp.desktop']),
	('share/pixmaps' , ['chirp.png']),
	('share/pixmaps' , ['chirp48.png'])]

setuptools.setup (
	name='chirp',
	version='0.1',
	scripts=['scripts/chirp'],
	packages=['chirp'],
	include_package_data = True,
	data_files=data,
	ext_package='chirp',
	author='George Pomortsev',
	author_email='illicium@gmail.com',
	description='Twitter desktop client',
	long_description='Python/GTK+ Twitter desktop client',
	license='MIT License',
	url='http://code.google.com/p/chirp',
	keywords='twitter desktop client gtk python',
	install_requires=['python-twitter'],
	zip_safe=False
)
