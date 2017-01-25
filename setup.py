from distutils.core import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='steamfront',
    version='0.0.1',
    description='A simple plugin to allow you to nicely access things on the Steam API and web server.',
    long_description=readme,
    author='Callum Bartlett',
    author_email='callum.b@techie.com',
    url='https://github.com/4Kaylum/Steamfront',
    download_url='',
    keywords=['steam', 'web', 'steamfront', 'steampowered'],
    classifiers=[],
    license=license
)

