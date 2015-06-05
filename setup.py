import setuptools


setuptools.setup(
    name='wock',
    version='0.1',
    description='a stupid wrapper for mock',
    author='Carl George',
    author_email='carl.george@rackspace.com',
    url='https://github.com/carlgeorge/wock',
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
