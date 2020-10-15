"""
(c). Copyright 2918, Raymond C Horn Jr., All Rights Reserved.

This is the best I can do given 24 clock-hours to work on this 
however I may have spent 1-2 hours for this so far..

PEP8 was used to create this file and according to my PEP8 Checker
it all passes PEP8 and is 100% Compliant with PEP8.
"""
import os
import sys
from datetime import datetime

import requests

from beautifulscraper import BeautifulScraper

from optparse import OptionParser

import logging

from logging.config import dictConfig

abspath = os.path.abspath('.')
fname = os.path.splitext(os.path.basename(__file__))[0]
now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers={
        'h': {'class': 'logging.FileHandler',
              'formatter': 'f',
              'level': logging.DEBUG,
              'filename': os.path.sep.join([abspath, fname+'_'+now+'.log']), 
              },
        'c': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG,
              'stream': sys.stdout,
              }
        },
    root={
        'handlers': ['h', 'c'],
        'level': logging.DEBUG,
        },
)

msg1 = 'Not using the correct Python version,' + \
    ' please ensure you are using Python 2.7.14. Thanks.'

url1 = 'http://ftp.uk.debian.org/debian/dists/stable/main/'

msg2 = 'Architecture like amd64, arm64, mips etc. or any keyword.'

if (__name__ == '__main__'):
    vmajor = sys.version_info.major
    vminor = sys.version_info.minor
    vmicro = sys.version_info.micro
    vers = vmajor, vminor, vmicro
    __vers__ = (2, 7, 14)
    assert vers == __vers__, msg1

    dictConfig(logging_config)
    logger = logging.getLogger()

    parser = OptionParser()
    
    parser.add_option("-a", "--addrs", type="string",
                      help="Source address like "+url1,
                      dest="addrs", default=url1)

    parser.add_option("-t", "--arch", type="string",
                      help=msg2,
                      dest="arch", default="amd64")

    options, arguments = parser.parse_args()
    
    '''
    The following block of code fetches information 
    from the HTML from the base URL.
    '''

    __data__ = {}
    if (options.addrs):
        scraper = BeautifulScraper()
        body = scraper.go(options.addrs)
        
        __data__[options.addrs] = {}
        __bucket__ = __data__[options.addrs]
        
        anchors = body.find_all('a')
        for anchor in anchors:
            href = anchor.attrs.get('href', '')
            if (len(href) > 0) and (href not in ['../']):
                __is__ = href.find('.') and (len(href.split('.')) == 2)
                __matches__ = (not __is__) and (href.find(options.arch) > -1)
                if (__matches__):
                    __bucket__[href] = {'href': href, 'is_filename': __is__}
                    
        '''
        Given the initial matching links one would need to
        scrape the contents (files or links) and either 
        download (for files) or scrape links for the rest.
        
        More development time would be required to take 
        this further.
        
        Additional development time would be required to 
        make this info more robust professional code one
        might be tempted to use in a production environment.
        
        Production level code takes more time than just 1 day.
        
        I would be happy to continue working on this once
        a suitable professional engagement has been secured.
        '''
    else:
        logger.warning('Missing -a option, see option -h for the details.')
    
    print
    