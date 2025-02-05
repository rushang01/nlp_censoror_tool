from setuptools import setup, find_packages

setup(
	name='censoror_tool',
	version='1.0',
	author='Rushang Sunil Chiplunkar',
	author_email='chiplun.rushangs@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
