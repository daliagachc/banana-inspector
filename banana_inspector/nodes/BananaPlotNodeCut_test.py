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
from useful_scit.imps2.defs import *

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
from BananaPlotNodeCut import BananaPlotNodeCut

# %%
from collections import OrderedDict

# %%
from .. import confg

# %%
fwS = {'pos': (0.0, 0.0),
 'bypass': False,
 'terminals': OrderedDict([('dataIn',
               {'io': 'in',
                'multi': False,
                'optional': False,
                'renamable': False,
                'removable': False,
                'multiable': False}),
              ('dataOut',
               {'io': 'out',
                'multi': False,
                'optional': False,
                'renamable': False,
                'removable': False,
                'multiable': False})]),
 'nodes': [{'class': 'BananaPlotNode',
   'name': 'b1',
   'pos': (9.676800000000014, 32.6592),
   'state': {'pos': (9.676800000000014, 32.6592),
    'bypass': False,
    'ctrl': {'type': 'group',
     'readonly': False,
     'visible': True,
     'enabled': True,
     'renamable': False,
     'removable': False,
     'strictNaming': False,
     'expanded': True,
     'syncExpanded': False,
     'title': None,
     'name': 'params',
     'value': None,
     'default': None,
     'children': OrderedDict([('t1',
                   {'type': 'float',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 't1',
                    'value': 1523862760.9054825,
                    'default': 1000000000.0}),
                  ('t2',
                   {'type': 'float',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 't2',
                    'value': 1523955984.5097337,
                    'default': 2000000000.0}),
                  ('t3',
                   {'type': 'float',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 't3',
                    'value': 2.0,
                    'default': 2.0}),
                  ('dock',
                   {'type': 'str',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 'dock',
                    'value': 'BPlotDuck',
                    'default': 'BPlotDuck'})])}}},
  {'class': 'BananaPlotNode',
   'name': 'b1c',
   'pos': (139.104, -92.53439999999998),
   'state': {'pos': (139.104, -92.53439999999998),
    'bypass': False,
    'ctrl': {'type': 'group',
     'readonly': False,
     'visible': True,
     'enabled': True,
     'renamable': False,
     'removable': False,
     'strictNaming': False,
     'expanded': True,
     'syncExpanded': False,
     'title': None,
     'name': 'params',
     'value': None,
     'default': None,
     'children': OrderedDict([('dock',
                   {'type': 'str',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 'dock',
                    'value': 'BnnPlotCut',
                    'default': 'BnnPlotCut'})])}}}],
 'connects': [('Input', 'dataIn', 'bnn-cut', 'dataIn'),
  ('bnn-full', 't2', 'bnn-cut', 't2'),
  ('Input', 'dataIn', 'bnn-full', 'dataIn'),
  ('bnn-full', 't1', 'bnn-cut', 't1')],
 'inputNode': {'pos': (-150.0, 0.0),
  'bypass': False,
  'terminals': OrderedDict([('dataIn',
                {'io': 'out',
                 'multi': False,
                 'optional': False,
                 'renamable': False,
                 'removable': False,
                 'multiable': False})])},
 'outputNode': {'pos': (300.0, 0.0),
  'bypass': False,
  'terminals': OrderedDict([('dataOut',
                {'io': 'in',
                 'multi': False,
                 'optional': False,
                 'renamable': False,
                 'removable': False,
                 'multiable': False})])}}

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

bn = BananaPlotNodeRegion('bnn-full')
bnc = BananaPlotNodeCut('bnn-cut')

mw = QtGui.QMainWindow()
da = pg.dockarea.DockArea()

mw.setCentralWidget(da)

mw.show()

daS ={'main': ('vertical',
  [('dock', 'BPlotDuck', {}),
   ('horizontal',
    [('dock', 'dck2', {}),
     ('vertical',
      [('tab',
        [('dock', 'BnnPlotCut', {}), ('dock', 'dck3', {})],
        {'index': 0}),
       ('dock', 'dck1', {})],
      {'sizes': [248, 242]})],
    {'sizes': [299, 1043]})],
  {'sizes': [248, 497]}),
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

confg.dock_area = da


pyqtgraph.functions.eq = true_eq.eq

fw.setInput(**{'dataIn':das['dndlDp']})

fw.connectTerminals(fw['dataIn'], bn['dataIn'])
fw.connectTerminals(fw['dataIn'], bnc['dataIn'])
fw.connectTerminals(bn['t1'], bnc['t1'])
fw.connectTerminals(bn['t2'], bnc['t2'])

da.restoreState(daS)
mw.setGeometry(QtCore.QRect(491, 53, 1070, 752))

# fw.restoreState(fwS)


# %%
open_idea(fw.addNode)

# %%
# fw.saveState()

# %%
