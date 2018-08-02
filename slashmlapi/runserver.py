#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os

__version__ = '0.1'

from slashmlapi import application

if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0')
