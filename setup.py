import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'mako',
    'psycopg2'
    ]

setup(name='confrm',
      version='0.0.1',
      description='Conference Resource Management',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[],
      author='Christopher Brown',
      author_email='io@henrian.com',
      url='',
      keywords='conference resource management',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='confrm',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = confrm:main
      [console_scripts]
      initialize_confrm_db = confrm.scripts.initializedb:main
      """,
      )

