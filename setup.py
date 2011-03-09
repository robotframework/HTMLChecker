from distutils.core import setup

setup(
    name='robotframework-htmlchecker',
    package_dir = {'': 'src'},
    packages=['HTMLChecker', 'HTMLChecker.lib'],
    version='0.1',
    url='https://github.com/robotframework/HTMLChecker',
    author='Robot Framework developers',
    author_email='robotframework@gmail.com'
)
