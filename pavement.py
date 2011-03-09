import os
import subprocess

from paver.easy import *
from paver.setuputils import setup

BASEDIR = os.path.dirname(__file__)
VERSION = 0.1

setup(
    name='robotframework-htmlchecker',
    package_dir = {'': 'src'},
    packages=['HTMLChecker', 'HTMLChecker.lib'],
    version=VERSION,
    url='https://github.com/robotframework/HTMLChecker',
    author='Robot Framework developers',
    author_email='robotframework@gmail.com'
)

@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass

@task
@needs('generate_setup', 'minilib', 'setuptools.command.bdist_wininst')
def bdist_wininst():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass

@task
def atest():
    testdir = os.path.join(BASEDIR, 'test')
    cmd = ['pybot', '-d', os.path.join(testdir, 'results'), testdir]
    env = os.environ
    env.update({'PYTHONPATH': 'src'})
    subprocess.call(cmd, shell=(os.sep=='\\'), env=env)

@task
def version():
    version_path = os.path.join(BASEDIR, 'src', 'HTMLChecker', 'version.py')
    with open(version_path, 'w') as verfile:
        verfile.write('''"This file is updated by running `paver version`."

VERSION="%s"
''' % VERSION)

