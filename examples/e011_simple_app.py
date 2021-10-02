'''simplest possible app
also the main lauout for the application
maybe it shold be a test at some point\
'''

import pyqtgraph as pg
import pyqtgraph.console
import pyqtgraph.dockarea
import pyqtgraph.flowchart
from pyqtgraph.Qt import QtWidgets

import banana_inspector.util.log_bnn as lg
from banana_inspector import confg
import banana_inspector.util.console

lg.ger.setLevel(10)


def set_int():
    from IPython import get_ipython
    try:
        get_ipython().magic('gui qt5')
        INT = True
        lg.ger.info('interactive')
        pass
        # INT = False

    except:
        INT = False
        lg.ger.info('not interactive')
    return INT


# INT = set_int()
INT = False



###################
import banana_inspector.apps.basic_app as app
app.mw.show()
###################

if INT is False:
    pg.exec()
if INT is True:
    pass
    confg.main_window.show()
