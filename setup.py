try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='fit-extract',
    version='1.3.1',
    description='Extracts data from EC-Lab .fit files',
    long_description=readme,
    author='Austin Luong',
    author_email='austin1995@gmail.com',
    url='https://github.com/austinluong/fit-extract',
    license=license,
    packages=['fit_extract'],
    install_requires=["pandas >= 0.18.1"],
    entry_points={
        'console_scripts': ['fit-extract=fit_extract.__main__:main']}
    )
