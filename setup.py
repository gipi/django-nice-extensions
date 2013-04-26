from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'django-nice-extensions',
    version = '1.0.0',
    description = 'Some simple django commands',
    license = 'BSD',
    long_description = read('README'),
    url = 'https://github.com/gipi/django-nice-extensions',

    author = 'Gianluca Pacchiella',
    author_email = 'gp@ktln2.org',

    packages = ['nice_extensions'],
    install_requires = [
        'django>=1.4',
        'django-extensions',
    ],

    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)
