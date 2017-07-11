from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='djatex',
    version='1.0.0',
    description='Generate pdf from latex in django',
#    long_description=long_description,
    url='https://bitbucket.org/marc_culler/django-latex',
    author='Marc Culler',
#    author_email='',
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Web Application',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django latex pdf',
    packages=['djatex'],
    install_requires=['django'],
)
