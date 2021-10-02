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
import banana_inspector.monkey_tool as mk_tool
import banana_inspector.node_setup

fc = confg.main_fchart
import xarray as xr
nais_da = xr.open_dataarray('../banana_inspector/data_example/nais_chc_data.nc')
fc.addTerminal('nais_in',**{'io':'in'})
fc.setInput(**{'nais_in':nais_da})
app.mw.show()

p = confg.par_tree



p['project dir'] = './proj_files'
p['file proj'] = './proj_files/ff1.cf'

mk_tool.open_project()
###################

if INT is False:
    pg.exec()
if INT is True:
    pass
    confg.main_window.show()
