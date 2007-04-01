import ez_setup
ez_setup.use_setuptools()
import setuptools

setuptools.setup (
	name='chirp',
	version='0.1',
        scripts=['scripts/chirp'],
        packages=['chirp'],
        package_dir = {'chirp': 'src'},
	author='George Pomortsev',
	author_email='illicium@gmail.com',
	description='Twitter desktop client',
	long_description='A desktop client for reading and submitting messages to Twitter',
	license='New BSD License',
	url='http://code.google.com/p/chirp',
	keywords='twitter desktop client gtk python',
	install_requires = ['python-twitter >= 0.2']
)
