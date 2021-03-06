#!/usr/bin/env python
import requests
import time
import yaml
import logging
from lib import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger('donuts-ddns')

def ddns_update(**kwargs):
    for i in kwargs['tokens']:
        logger.info(
            """Updating token: %s"""
        %i)
        api = '%s/?hash=%s&ip=%s' %(kwargs['ws'], i, kwargs['ip'])
        try:
            res = requests.get(api, verify=False)
            logger.debug(
                """%s: just updated (%s) - %s"""
            %(i, kwargs['ip'], res.content))
        except:
            logger.debug(
                """%s: could not been updated (%s)"""
            %(i, kwargs['ip']))
    return True

def run(options):
    if options['daemon'] == True:
        ival = options.get('interval', 300)
        while True:
            myip = IPgetter().myip()
            for i in options['accounts']:
                logger.info('Trying with account: %s' %i)
                newopt = options.copy()
                newopt.pop('accounts')
                newopt.update(**options['accounts'][i])
                ddns_update(ip=myip, **newopt)
            logger.info(
                """Sleeping %s seconds to attempt to update again."""
            %ival)
            time.sleep(ival)
    else:
        myip = IPgetter().myip()
        for i in options['accounts']:
            newopt = options.copy()
            newopt.pop('accounts')
            newopt.update(**options['accounts'][i])
            ddns_update(ip=myip, **newopt)

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config",
                      help="Configuration file.", metavar="CONFIG")
    parser.add_option("-d", "--daemon", dest="daemon", default=False,
                      action="store_true",
                      help="Run as a daemon.")
    parser.add_option("-i", "--interval", dest="interval", default=300,
                      help="Configuration file", metavar="INTERVAL")
    parser.add_option("-t", "--token", dest="token",
                      help="Configuration file", metavar="TOKEN")
    parser.add_option("-w", "--webservice", dest="ws",
                      help="Webservice to commit", metavar="WEBSERVICE")
    parser.add_option("-q", "--quiet", dest="verbose", default=True,
                      action="store_false",
                      help="Don't print status messages to stdout.")
    (options, args) = parser.parse_args()

    if options.config:
        with open(options.config, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
            cfg.setdefault('logfile', '/var/log/donuts-ddns.log')
            cfg.setdefault('loglevel', 'info')
            cfg.setdefault('logformat',
            """%(asctime)s - %(name)s - %(levelname)s - %(message)s""")
            cfg.setdefault('interval', 300)
            cfg['daemon']  = options.daemon
            cfg['quiet']   = options.verbose
            handler = logging.FileHandler(cfg['logfile'])
            handler.setFormatter(logging.Formatter(cfg['logformat'],
                                                   "%Y-%m-%d %H:%M:%S"))
            logger.addHandler(handler)
            logger.setLevel(getattr(logging, cfg.get('loglevel').upper()))
    else:
        cfg = {'interval': options.interval,
               'daemon': options.daemon,
               'quiet': options.verbose,
               'accounts':
               {'dry':
                {'ws': options.ws,
                 'tokens': options.tokens}
               }
        }
    run(cfg)
    
if __name__ == '__main__':
    main()
