import pyqtgraph as pg
import banana_inspector as bi
from banana_inspector import confg

import numpy as np
import pyqtgraph as pg
import pyqtgraph.dockarea
import pyqtgraph.flowchart
import xarray as xr
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtWidgets
import banana_inspector.util.log_bnn as lg

lg.ger.setLevel(10)

from IPython import get_ipython
try:
    get_ipython().magic('gui qt5')
    INT = True
    lg.ger.info('interactive')

except:
    INT = False
    lg.ger.info('not interactive')

confg.main_window = mw = QtGui.QMainWindow()
confg.dock_area = da = pg.dockarea.DockArea()
confg.main_fchart = fc = pg.flowchart.Flowchart()
d1 = pg.dockarea.Dock('mnk-tool')
d2 = pg.dockarea.Dock('dummy')
d3 = pg.dockarea.Dock('flow-chart')

mw.setCentralWidget(da)
da.addDock(d1)
da.addDock(d2)
da.addDock(d3)




if INT is False:
    pg.exec()
if INT is True:
    confg.main_window.show()

