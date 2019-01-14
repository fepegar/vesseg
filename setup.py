from setuptools import setup

setup(
    name='vesseg',
    version='0.2.0',
    author='Fernando Perez-Garcia',
    author_email='fernando.perezgarcia.17@ucl.ac.uk',
    install_requires=[
        'click',
        'tensorflow-gpu',
        'niftynet',
        'SimpleITK',
        'vtk',
    ],
    entry_points={
        'console_scripts': [
            'vesseg=segment:main',
            'bin2mesh=bin2mesh:main',
        ],
    },
)
