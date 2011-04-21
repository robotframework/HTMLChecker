import os
from os.path import join as _join
from subprocess import call

from paver.easy import *
from paver.setuputils import setup

BASEDIR = os.path.dirname(__file__)
VERSION = '0.3'

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
def atest():
    testdir = _join(BASEDIR, 'test')
    _sh(['pybot', '-d', _join(testdir, 'results'), testdir])

@task
def version():
    version_path = _join(BASEDIR, 'src', 'HTMLChecker', 'version.py')
    with open(version_path, 'w') as verfile:
        verfile.write('''"This file is updated by running `paver version`."
VERSION="%s"
''' % VERSION)

@task
@needs('version')
def doc():
    libdoc = _join(BASEDIR, 'lib', 'libdoc.py')
    docdir = _get_dir('doc')
    _sh(['python', libdoc , '-o', '%s/HTMLChecker-%s.html' % (docdir, VERSION),
         'HTMLChecker'])

@task
@needs('version', 'sdist', 'doc')
def release():
    _sh(['git', 'ci', '-a', '-m', 'updated version'])
    _sh(['git', 'tag', VERSION])
    print 'Created git tag for %s' % VERSION
    print 'Windows installer has to be created with `paver bdist_wininst`'
    print 'Remember to `git push --tags` and upload sdist & doc to GitHub'


def _sh(cmd):
    env = os.environ
    env.update({'PYTHONPATH': 'src'})
    call(cmd, shell=(os.sep=='\\'), env=env)

def _get_dir(name):
    dirname = _join(BASEDIR, name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname
