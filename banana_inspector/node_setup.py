

import numpy as np
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui





from .nodes.BananaPlotNodeRegion import BananaPlotNodeRegion
from .nodes.BananaPlotNodeCut import BananaPlotNodeCut
from .nodes.SliceBnnNode import SliceBnnNode
from .nodes.BnnSlicesPlotNode import BnnSlicesPlotNode
from .nodes.RegridBnnNode import RegridBnnNode
from .nodes.DeUtcNode import DeUtcNode
from .nodes.CombineSpectraNode import CombineSpectraNode
from .nodes.PeelNode_scratch import PeelNode
from .nodes.GaussianFilterNode import GaussianFilterNode
from .nodes.QNormFilterNode import QNormFilterNode

from . import confg
import pyqtgraph.console

from collections import OrderedDict

# %%
# das = xr.open_dataarray('../data_out/test_data/da.nc')

# %%
# das

# %%

# %%
import pyqtgraph.flowchart.library as fclib

# %%
# open_idea(SliceBnnNode)


library = fclib.NodeLibrary()
empty = fclib.NodeLibrary()

fw = confg.main_fchart

library.addNodeType(    BananaPlotNodeRegion    , [(    'Display'   ,)])
library.addNodeType(    BananaPlotNodeCut       , [(    'Display'   ,)])
library.addNodeType(    BnnSlicesPlotNode       , [(    'Display'   ,)])
library.addNodeType(    RegridBnnNode           , [(    'Data'      ,)])
library.addNodeType(    SliceBnnNode            , [(    'Data'      ,)])
library.addNodeType(    DeUtcNode               , [(    'Data'      ,)])
library.addNodeType(    CombineSpectraNode      , [(    'Data'      ,)])

library.addNodeType(    PeelNode                , [(    'Peel'      ,)])
library.addNodeType(    GaussianFilterNode      , [(    'Filter'    ,)])
library.addNodeType(    QNormFilterNode         , [(    'Filter'    ,)])

# Add the unsharp mask node to two locations in the menu to demonstrate
# that we can create arbitrary menu structures
# library.addNodeType(UnsharpMaskNode, [('Image',),
#                                       ('Submenu_test','submenu2','submenu3')])

fw.setLibrary(empty)
fw.setLibrary(library)











