from setuptools import setup

with open("acquantumconnector/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

with open('README.rst', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

info = {
    'name': 'acquantum-connector',
    'version': version,
    'author': 'Carsten Blank',
    'author_email': 'blank@data-cybernetics.com',
    'description': '',
    'long_description': long_description,
    'url': 'https://github.com/carstenblank/acquantum-connector',
    'packages': [
        'acquantumconnector',
        'acquantumconnector.connector',
        'acquantumconnector.credentials',
        'acquantumconnector.model',
    ],
    'install_requires': requirements,
    'license': 'Apache 2.0',
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
]

setup(classifiers=classifiers, **info)
