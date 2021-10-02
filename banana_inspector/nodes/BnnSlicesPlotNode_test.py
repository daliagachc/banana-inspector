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
das = xr.open_dataarray('../data_out/test_data/da.nc')

# %%
das

# %%
from BananaPlotNodeRegion import BananaPlotNodeRegion
from BananaPlotNodeCut import BananaPlotNodeCut
from SliceBnnNode import SliceBnnNode
from BnnSlicesPlotNode import BnnSlicesPlot, BnnSlicesPlotNode

# %%
from .. import confg

# %%
bnn_slice_p = BnnSlicesPlot()

# %%
bnn_slice_p.set_up_plots(das)

# %%
bnn_slice_p.plot_curves((100,100,100),das)

# %%
bnn_slice_p.grid_layout.show()

# %%
len(bnn_slice_p.Dps)

# %%
bnn_slice_p.widger_layout.show()

# %%
import pyqtgraph.console

# app = pg.mkQApp()

## build an initial namespace for console commands to be executed in (this is optional;
## the user can always import these modules manually)
namespace = {'pg': pg, 'np': np, 'app': confg}

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

bn = BananaPlotNodeRegion('bnn-full')
bnc = BananaPlotNodeCut('bnn-cut')
sbnn = SliceBnnNode('slice-bnb')
slices_plot_node = BnnSlicesPlotNode('bnn_slices_node')

mw = QtGui.QMainWindow()
da = pg.dockarea.DockArea()

mw.setCentralWidget(da)

mw.show()

daS ={'main': ('horizontal',
  [('vertical',
    [('dock', 'BPlotDuck', {}),
     ('horizontal',
      [('dock', 'dck2', {}),
       ('vertical',
        [('tab',
          [('dock', 'BnnPlotCut', {}), ('dock', 'dck3', {})],
          {'index': 0}),
         ('dock', 'dck1', {})],
        {'sizes': [329, 321]})],
      {'sizes': [259, 903]})],
    {'sizes': [329, 657]}),
   ('dock', 'BnnSlicesDock', {})],
  {'sizes': [1169, 500]}),
 'float': []}



dck1 = pg.dockarea.Dock('dck1')
dck2 = pg.dockarea.Dock('dck2')

dck1.addWidget(c)

da.addDock(dck1)
da.addDock(dck2)

dck3 = pg.dockarea.Dock('dck3')

da.addDock(dck3)




fw = pg.flowchart.Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})

w = fw.widget()

dck2.addWidget(w)

fw.addNode(bn,name='b1')
fw.addNode(bnc,name='b1c')
fw.addNode(sbnn,name='slice_bnn')
fw.addNode(slices_plot_node,name='slices-plot-node')

confg.dock_area = da


pyqtgraph.functions.eq = true_eq.eq

fw.setInput(**{'dataIn':das})

fw.connectTerminals(fw['dataIn'], bn['dataIn'])
fw.connectTerminals(bn['t1'], sbnn['t1'])
fw.connectTerminals(bn['t2'], sbnn['t2'])

fw.connectTerminals(sbnn['dataOut'], bnc['dataIn'])
fw.connectTerminals(sbnn['dataOut'], slices_plot_node['dataIn'])
fw.connectTerminals(fw['dataIn'], sbnn['dataIn'])

da.restoreState(daS)
mw.setGeometry(QtCore.QRect(491, 53, 1070, 752))

# fw.restoreState(fwS)


# %%
da.saveState()

# %%
