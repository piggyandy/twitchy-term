#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
	name='twitchy-term',
	version='1.0.0',
	description='A command line interface for browsing/streaming on Twitch.tv.',
	long_description=open('README.rst').read(),
	url='https://github.com/Andy-Au/twitchy-term',
	author='Andy Au',
	author_email='au.andy.ch@gmail.com',
	license='MIT',
	keywords='twitch livestreamer command line interface terminal stream',
	classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console :: Curses',
        'Operating System :: POSIX',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Terminals',
        'Topic :: Games/Entertainment',
        ],
    packages=find_packages(),
    install_requires=['livestreamer'],
	entry_points={
        'console_scripts': [
            'twitchy-term=twitchyterm.__main__:main',
        ],
    },
)


