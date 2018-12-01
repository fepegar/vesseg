from setuptools import setup

setup(
    name='vesseg',
    version='0.1.0',
    author='Fernando Perez-Garcia',
    author_email='fernando.perezgarcia.17@ucl.ac.uk',
    install_requires=[
        'click',
        'tensorflow-gpu',
        'niftynet',
    ],
    entry_points={
        'console_scripts': [
            'vesseg=segment:main',
        ],
    },
)
