import os
from setuptools import setup, find_packages
from pyutils import VERSION, DEV_STATUS

setup(
    name='lmn_pyutils',
    version='.'.join(map(str, VERSION)),
    description='Various Python utilities for text and date handling',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    keywords='python utils dates text',
    author='Michael Bourke',
    author_email='git@elementality.com',
    url='https://github.com/lmntality/pyutils',
    license='MIT license',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'lmn_pyutils': ['pyutils'],
    },
    classifiers=[
        'Development Status :: %s' % DEV_STATUS,
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    install_requires=[
        'python-dateutil',
        'pytz',
        'pyRFC3339',
        'chardet'
    ],
)
