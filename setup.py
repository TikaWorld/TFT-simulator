# encoding: utf-8
from setuptools import setup, find_packages


setup(
    name='tft',
    version='0.1',
    author='Seungchae Na',
    author_email='tikaworld0416@gmail.com',
    description='TeamFight Tactics Simulator.',
    install_requires=['simpy==4.0.1'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
