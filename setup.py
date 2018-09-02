from setuptools import setup

with open('README.md', "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='aionewsapi',
    version='1.1.1',
    author='Marc Ford',
    url='https://github.com/mfdeux/aionewsapi',
    description='Asyncio client for interacting with newsapi.org',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['aionewsapi'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp',
        'uvloop',
        'marshmallow',
        'python-dateutil'
    ]
)

setup(**setup_args)
