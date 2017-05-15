import os
from setuptools import setup, find_packages

short_description = 'Client for Hunter REST API'
long_description = short_description

if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='hunter_python',
    version='2.0.0',
    description=short_description,
    long_description=long_description,
    license='MIT',
    keywords='hunter client rest api cli',
    author='Alan Vezina',
    author_email='alan.vezina@gmail.com',
    url='https://github.com/tipsqueal/hunter-python',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points='''
    [console_scripts]
    hunter=hunter.cli:main
    ''',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ]
)
