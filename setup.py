import os
import setuptools
from src.cdb.version import __version__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cdb',
    version=__version__,
    author='David Watson',
    author_email='david.watson@tyme.com',
    description='Card Deck Builder',
    long_description='Print a Deck of Cards',
    long_description_content_type='text/markdown',
    url='none',
    # py_modules=['box', 'card_back', 'card_box', 'card_types', 'card_type_provider', 'card', 'cdb', 'database', 'deck_builder', 'deck_renderer', 'deck', 'exceptions', 'fitting', 'font_style', 'image', 'library_loader', 'library', 'padding', 'paragraph', 'point', 'position', 'style', 'types', 'version'],
    install_requires=[
        'Click',
        'reportlab',
        'PyYAML',
        'deepmerge'
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
            "cdb = cdb.cdb:cli"
        ]
    }
)
