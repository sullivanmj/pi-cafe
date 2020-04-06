from setuptools import setup
from os import path

import picafe

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='picafe',
    version=picafe.__version__,
    url='http://github.com/sullivanmj/picafe/',
    license='MIT License',
    author='Matt Sullivan',
    tests_require=['pytest', ],
    install_requires=['pywemo>=0.4,<0.5', ],
    description='Automated REST APIs for existing database-driven systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['picafe'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    python_requires='>=3.7',
)