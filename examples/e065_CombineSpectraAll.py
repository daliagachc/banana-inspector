'''simplest possible app
also the main lauout for the application
maybe it shold be a test at some point\
'''
import os
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
# nais_da = xr.open_dataarray('../banana_inspector/data_example/nais_chc_data.nc')
# smps_da = xr.open_dataarray('../banana_inspector/data_example/smps_chc_data.nc')

dp = '../banana_inspector/data_example'

smps_chc_data  = xr.open_dataarray(os.path.join(dp,'smps_chc_data.nc'))
nais_nP_chc    = xr.open_dataarray(os.path.join(dp,'nais_nP_chc.nc'  ))
nais_pP_chc    = xr.open_dataarray(os.path.join(dp,'nais_pP_chc.nc'  ))
nais_nI_chc    = xr.open_dataarray(os.path.join(dp,'nais_nI_chc.nc'  ))
nais_pI_chc    = xr.open_dataarray(os.path.join(dp,'nais_pI_chc.nc'  ))

fc.addTerminal('smps_chc_data',**{'io':'in'})
fc.addTerminal('nais_nP_chc'  ,**{'io':'in'})
fc.addTerminal('nais_pP_chc'  ,**{'io':'in'})
fc.addTerminal('nais_nI_chc'  ,**{'io':'in'})
fc.addTerminal('nais_pI_chc'  ,**{'io':'in'})

fc.setInput(**{'smps_chc_data':smps_chc_data})
fc.setInput(**{'nais_nP_chc'  :nais_nP_chc  })
fc.setInput(**{'nais_pP_chc'  :nais_pP_chc  })
fc.setInput(**{'nais_nI_chc'  :nais_pI_chc  })
fc.setInput(**{'nais_pI_chc'  :nais_pI_chc  })

app.mw.show()

p = confg.par_tree



p['project dir'] = './proj_files'
p['file proj'] = './proj_files/CombineSpectraAll2.cf'

try:
    mk_tool.open_project()
    pass
except:
    pass
###################

if INT is False:
    pg.exec()
if INT is True:
    pass
    confg.main_window.show()
