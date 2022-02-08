import os
import setuptools
from src.cdp.version import __version__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cdp',
    version=__version__,
    author='David Watson',
    author_email='david.watson@tyme.com',
    description='Card Deck Printer',
    long_description='Print a Deck of Cards',
    long_description_content_type='text/markdown',
    url='none',
    install_requires=[
        'Click',
        'reportlab',
        'PyYAML',
        'deepmerge',
        'requests'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: None',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "cdp = cdp.cdp:cli"
        ]
    }
)
