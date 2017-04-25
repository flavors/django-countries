import os
import re

from setuptools import setup, find_packages


def get_long_description():
    for filename in ('README.rst', 'HISTORY.rst'):
        with open(filename, 'r') as f:
            yield f.read()


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='countries-flavor',
    version=get_version('countries_flavor'),
    license='MIT',
    description='Django countries app',
    long_description='\n\n'.join(get_long_description()),
    author='mongkok',
    author_email='dani.pyc@gmail.com',
    maintainer='mongkok',
    url='https://github.com/flavors/countries/',
    packages=find_packages(exclude=['tests*']),
    install_requires=['Django>=1.8'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
    zip_safe=False,
    tests_require=['Django>=1.8'],
    package_data={
        'countries_flavor': [
            'locale/*/LC_MESSAGES/django.po',
            'locale/*/LC_MESSAGES/django.mo'
        ]
    }
)