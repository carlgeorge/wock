import setuptools


setuptools.setup(
    name='wock',
    version='0.1',
    description='wrapper for mock',
    author='Carl George',
    author_email='carl.george@rackspace.com',
    url='https://github.rackspace.com/carl-george/wock',
    packages=['wock'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'wock = wock:cli'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4'
    ]
)
