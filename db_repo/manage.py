#!/usr/bin/env python
import os
import sys
from ConfigParser import ConfigParser
from migrate.versioning.shell import main

if __name__ == '__main__':
    config = ConfigParser(dict(here=os.getcwd()))
    config.read([arg.replace('--config=', '') for arg in sys.argv if arg.endswith('.ini')][0])
    app_config = dict(config.items('app:main'))

    main(url=app_config['sqlalchemy.url'], debug='False', repository='db_repo')
