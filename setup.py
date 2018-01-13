import os
import re

from setuptools import find_packages, setup


def get_long_description():
    for filename in ('README.rst',):
        with open(filename, 'r') as f:
            yield f.read()


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='django-countries-flavor',
    version=get_version('countries'),
    license='MIT',
    description='A Django application that provides a data collection '
    'for internationalization and localization purposes.',
    long_description='\n\n'.join(get_long_description()),
    author='mongkok',
    author_email='domake.io@gmail.com',
    maintainer='mongkok',
    url='https://github.com/flavors/django-countries/',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=1.9',
        'psycopg2>=2.6.2',
        'requests>=1.1.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
    ],
    zip_safe=False,
    tests_require=[
        'Django>=1.9',
        'factory-boy>=2.8.1',
        'psycopg2>=2.6.2',
        'requests>=1.1.0',
    ],
    package_data={
        'countries': [
            'fixtures/**/*.json',
            'locale/*/LC_MESSAGES/django.po',
            'locale/*/LC_MESSAGES/django.mo',
        ],
    },
)
