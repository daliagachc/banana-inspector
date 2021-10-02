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

from BananaPlotNodeRegion import BananaPlotNodeRegion
from BananaPlotNodeCut import BananaPlotNodeCut
from SliceBnnNode import SliceBnnNode
from BnnSlicesPlotNode import BnnSlicesPlotNode
from RegridBnnNode import RegridBnnNode

from .. import confg
import pyqtgraph.console

from collections import OrderedDict

# %%
das = xr.open_dataarray('../data_out/test_data/da.nc')

# %%
das

# %%

# %%
import pyqtgraph.flowchart.library as fclib

# %%
# open_idea(SliceBnnNode)

# %%
library = fclib.LIBRARY.copy() # start with the default node set

# %%
# fw.saveState()

# %%
fS = {'pos': (0.0, 0.0),
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
 'nodes': [{'class': 'BananaPlotNodeRegion',
   'name': 'BananaPlotNodeRegion.0',
   'pos': (-53.82720000000003, -104.02560000000003),
   'state': {'pos': (-53.82720000000003, -104.02560000000003),
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
                    'value': 1522585175.7524345,
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
                    'value': 1523247543.5216708,
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
                    'value': 9.0,
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
                    'value': 'BPlotDuck1',
                    'default': 'BPlotDuck'})])}}},
  {'class': 'SliceBnnNode',
   'name': 'SliceBnnNode.0',
   'pos': (67.13279999999997, 44.15039999999996),
   'state': {'pos': (67.13279999999997, 44.15039999999996),
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
     'default': None}}},
  {'class': 'RegridBnnNode',
   'name': 'RegridBnnNode.0',
   'pos': (104.02559999999988, -84.67200000000001),
   'state': {'pos': (104.02559999999988, -84.67200000000001),
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
     'children': OrderedDict([('n_subs',
                   {'type': 'int',
                    'readonly': False,
                    'visible': True,
                    'enabled': True,
                    'renamable': False,
                    'removable': False,
                    'strictNaming': False,
                    'expanded': True,
                    'syncExpanded': False,
                    'title': None,
                    'name': 'n_subs',
                    'value': 11,
                    'default': 11}),
                  ('log_dx',
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
                    'name': 'log_dx',
                    'value': 0.05,
                    'default': 0.5})])}}},
  {'class': 'BananaPlotNodeCut',
   'name': 'BananaPlotNodeCut.0',
   'pos': (273.3695999999999, 57.45599999999999),
   'state': {'pos': (273.3695999999999, 57.45599999999999),
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
                    'default': 'BnnPlotCut'})])}}},
  {'class': 'BnnSlicesPlotNode',
   'name': 'BnnSlicesPlotNode.0',
   'pos': (283.4576000000001, -108.1576),
   'state': {'pos': (283.4576000000001, -108.1576),
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
                    'value': 'BnnSlicesDock1',
                    'default': 'BnnSlicesDock'})])}}}],
 'connects': [('BananaPlotNodeRegion.0', 't2', 'SliceBnnNode.0', 't2'),
  ('SliceBnnNode.0', 'dataOut', 'RegridBnnNode.0', 'dataIn'),
  ('BananaPlotNodeRegion.0', 't1', 'SliceBnnNode.0', 't1'),
  ('RegridBnnNode.0', 'dataOut', 'BananaPlotNodeCut.0', 'dataIn'),
  ('Input', 'dataIn', 'SliceBnnNode.0', 'dataIn'),
  ('RegridBnnNode.0', 'dataOut', 'BnnSlicesPlotNode.0', 'dataIn'),
  ('Input', 'dataIn', 'BananaPlotNodeRegion.0', 'dataIn')],
 'inputNode': {'pos': (-150.0, 0.0),
  'bypass': False,
  'terminals': OrderedDict([('dataIn',
                {'io': 'out',
                 'multi': False,
                 'optional': False,
                 'renamable': False,
                 'removable': False,
                 'multiable': False})])},
 'outputNode': {'pos': (295.7664000000002, -26.006399999999985),
  'bypass': False,
  'terminals': OrderedDict([('dataOut',
                {'io': 'in',
                 'multi': False,
                 'optional': False,
                 'renamable': False,
                 'removable': False,
                 'multiable': False})])}}

# %%
library = fclib.NodeLibrary()
empty = fclib.NodeLibrary()

fw = pg.flowchart.Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})

library.addNodeType(BananaPlotNodeRegion, [('Display',)])
library.addNodeType(BananaPlotNodeCut, [('Display',)])
library.addNodeType(BnnSlicesPlotNode, [('Display',)])


library.addNodeType(RegridBnnNode, [('Data',)])
library.addNodeType(SliceBnnNode, [('Data',)])

# Add the unsharp mask node to two locations in the menu to demonstrate
# that we can create arbitrary menu structures
# library.addNodeType(UnsharpMaskNode, [('Image',),
#                                       ('Submenu_test','submenu2','submenu3')])

fw.setLibrary(empty)
fw.setLibrary(library)



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
    # noinspection PyUnresolvedReferences
    mw.close()
except:
    pass 

# bn = BananaPlotNodeRegion('bnn-full')
# bnc = BananaPlotNodeCut('bnn-cut')
# sbnn = SliceBnnNode('slice-bnb')
# slices_plot_node = BnnSlicesPlotNode('bnn_slices_node')
# regrid_node = RegridBnnNode('regrid_node')



# bn               = fw.createNode('BananaPlotNodeRegion')
# bnc              = fw.createNode('BananaPlotNodeCut')
# sbnn             = fw.createNode('SliceBnnNode')
# slices_plot_node = fw.createNode('BnnSlicesPlotNode')
# regrid_node      = fw.createNode('RegridBnnNode')

mw = QtGui.QMainWindow()
da = pg.dockarea.DockArea()

mw.setCentralWidget(da)

mw.show()

daS ={'main': ('vertical',
  [('dock', 'BPlotDuck1', {}),
   ('horizontal',
    [('horizontal',
      [('dock', 'dck2', {}),
       ('vertical',
        [('tab',
          [('dock', 'BnnPlotCut', {}), ('dock', 'dck3', {})],
          {'index': 0}),
         ('dock', 'dck1', {})],
        {'sizes': [248, 242]})],
      {'sizes': [222, 612]}),
     ('dock', 'BnnSlicesDock1', {})],
    {'sizes': [841, 423]})],
  {'sizes': [248, 497]}),
 'float': []}



dck1 = pg.dockarea.Dock('dck1')
dck2 = pg.dockarea.Dock('dck2')

dck1.addWidget(c)

da.addDock(dck1)
da.addDock(dck2)

dck3 = pg.dockarea.Dock('dck3')

da.addDock(dck3)





w = fw.widget()

dck2.addWidget(w)

# fw.addNode(bn,name='b1')
# fw.addNode(bnc,name='b1c')
# fw.addNode(sbnn,name='slice_bnn')
# fw.addNode(slices_plot_node,name='slices-plot-node')

# fw.addNode(regrid_node, name='regrio-node')

confg.dock_area = da


pyqtgraph.functions.eq = true_eq.eq



# fw.connectTerminals(fw['dataIn'], bn['dataIn'])
# fw.connectTerminals(bn['t1'], sbnn['t1'])
# fw.connectTerminals(bn['t2'], sbnn['t2'])

# fw.connectTerminals(sbnn['dataOut'], bnc['dataIn'])
# fw.connectTerminals(sbnn['dataOut'], slices_plot_node['dataIn'])
# fw.connectTerminals(fw['dataIn'], sbnn['dataIn'])


fw.setInput(**{'dataIn':das})

fw.restoreState(fS)
da.restoreState(dS)
mw.setGeometry(QtCore.QRect(491, 53, 1070, 752))


