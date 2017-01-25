from setuptools import setup, find_packages

with open('PyPI_README.rst') as a:
    long_description = a.read()

setup(
    name='steamfront',
    version='0.0.2',
    description='A simple plugin to allow you to nicely access things on the Steam API and web server.',
    long_description=long_description,
    author='Callum Bartlett',
    author_email='callum.b@techie.com',
    license='mit',
    url='https://github.com/4Kaylum/Steamfront',
    download_url='https://github.com/4Kaylum/Steamfront/tarball/0.0.1',
    keywords='steam web steamfront steampowered',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Internet',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=['requests'],
    packages=find_packages()
)

