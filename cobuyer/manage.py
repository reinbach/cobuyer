#!/usr/bin/env python
import imp
import os
import sys

from django.core.management import execute_manager

try:
    imp.find_module('settings')
except ImportError:
    sys.stderr.write("Error: Can't find the 'settings' module in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
