try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fitExtract',
    version='1.0',
    description='Extracts data from EC-Lab .fit files',
    long_description=readme,
    author='Austin Luong',
    author_email='austin1995@gmail.com',
    url='https://github.com/austinluong/fitExtract',
    license=license,
    packages=['fitExtract'],
    install_requires=['pandas'],
    package_data={'': ['README.md', 'LICENSE']})
