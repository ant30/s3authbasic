import os

from setuptools import setup, find_packages

VERSION = '0.1.2'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'boto',
]

test_requires = [
    'WebTest',
]

test_requires_extras = test_requires + [
    'nose',
    'coverage',
]


setup(name='s3authbasic',
      version=VERSION,
      description='s3authbasic',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Antonio Perez-Aranda Alcaide',
      author_email='ant30tx@gmail.com',
      url='http://www.ant30.es/',
      download_url='https://github.com/ant30/s3authbasic/'
                   'tarball/{0}'.format(VERSION),
      keywords='web pyramid pylons s3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require={
          'testing': test_requires_extras,
      },
      test_suite="s3authbasic",
      entry_points="""\
      [paste.app_factory]
      main = s3authbasic:main
      [console_scripts]
      run-s3authbasic = s3authbasic.runapp:main
      """,
      )
