# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python [conda env:q5]
#     language: python
#     name: conda-env-q5-py
# ---

# %%

# %%
# %%

import numpy as np
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui


from IPython import get_ipython
try:
    get_ipython().magic('gui qt5')
    INT = True
except:
    INT = False

import true_eq

# %%
das = xr.open_dataset('../data_out/test_data/da.nc')

# %%
from BananaPlotNodeRegion import BananaPlotNodeRegion

# %%
from .. import confg

# %%
import pyqtgraph.console

# app = pg.mkQApp()

## build an initial namespace for console commands to be executed in (this is optional;
## the user can always import these modules manually)
namespace = {'pg': pg, 'np': np}

## initial text to display in the console
text = """
This is an interactive python console. The numpy and pyqtgraph modules have already been imported 
as 'np' and 'pg'. 

Go, play.
"""
c = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)

try:
    mw.close()
except:
    pass 

bn = BananaPlotNodeRegion('b1')

mw = QtGui.QMainWindow()
da = pg.dockarea.DockArea()

mw.setCentralWidget(da)

mw.show()

daS = {'main': ('horizontal',
  [('dock', 'dck2', {}),
   ('vertical',
    [('dock', 'dck3', {}), ('dock', 'dck1', {})],
    {'sizes': [463, 462]})],
  {'sizes': [247, 564]}),
 'float': []}



dck1 = pg.dockarea.Dock('dck1')
dck2 = pg.dockarea.Dock('dck2')

dck1.addWidget(c)

da.addDock(dck1)
da.addDock(dck2)

dck3 = pg.dockarea.Dock('dck3')

da.addDock(dck3)

da.restoreState(daS)


fw = pg.flowchart.Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})

w = fw.widget()

dck2.addWidget(w)

fw.addNode(bn,name='b1')

confg.dock_area = da


pyqtgraph.functions.eq = true_eq.eq

fw.setInput(**{'dataIn':das['dndlDp']})

fw.connectTerminals(fw['dataIn'], bn['dataIn'])

mw.setGeometry(QtCore.QRect(491, 53, 1070, 752))


# %%

# %%
bn.bp

# %%
