# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''
this module tryes to make logging easier
# >>> import useful_scit.util.log as log
# >>> log.ger.setLevel(log.log.DEBUG)
# >>> log.ger.debug('leg.ger level is %s', log.log.DEBUG)
# >>> log.ger.info('this message wont be shown')
# >>> log.ger.setLevel(log.log.INFO)
# >>> log.ger.info('now this message is shown')
# >>> log.ger.debug('so is this one')
# >>> log.print_levels()
'''

import logging as log
import sys

# log = log
ger = log.getLogger('Bnn')
handler = log.StreamHandler()
formatter = log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
ger.addHandler(handler)

ger_out = log.getLogger('Bnn')
handler = log.StreamHandler(sys.stdout)
formatter = log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
ger_out.addHandler(handler)
# ger.setLevel(logging.DEBUG)

ger1 = log.getLogger('Bnn1')
handler = log.StreamHandler()
formatter = log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
ger1.addHandler(handler)

# logger.debug('often makes a very good meal of %s', 'visiting tourists')


LEVELS = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'FATAL'
]

def print_levels():
    for l in LEVELS:
        print(l, getattr(log, l))
