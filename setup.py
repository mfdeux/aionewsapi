from setuptools import setup

setup_args = dict(
    name='aionewsapi',
    version='1.1.0',
    author='Marc Ford',
    url='https://github.com/mfdeux/aionewsapi',
    description='Asyncio client for interacting with newsapi.org',
    long_description='',
    license='MIT',
    packages=['aionewsapi'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'aiohttp',
        'uvloop',
        'marshmallow',
        'python-dateutil'
    ]
)

setup(**setup_args)
