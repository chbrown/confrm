#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql://localhost/confrm_dev', debug='False', repository='db_repo')
