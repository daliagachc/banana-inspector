

import numpy as np
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui





from .nodes.BananaPlotNodeRegion import BananaPlotNodeRegion
from .nodes.BananaPlotNodeCut import BananaPlotNodeCut
from .nodes.BananaPlotNodeCut2 import BananaPlotNodeCut2
from .nodes.SliceBnnNode import SliceBnnNode
from .nodes.BnnSlicesPlotNode import BnnSlicesPlotNode
from .nodes.RegridBnnNode import RegridBnnNode
from .nodes.DeUtcNode import DeUtcNode
from .nodes.CombineSpectraNode import CombineSpectraNode
from .nodes.PeelNode import PeelNode
from .nodes.GaussianFilterNode import GaussianFilterNode
from .nodes.AdaptativeFilterNode import AdaptativeFilterNode
from .nodes.QNormFilterNode import QNormFilterNode
from .nodes.RidgeFilterNode import RidgeFilterNode
from .nodes.FileOpenerNode import FileOpenerNode
from .nodes.ConcatTimeNode import ConcatTimeNode
from .nodes.FileSaverNode import FileSaverNode
from .nodes.CutDpNode import CutDpNode
from .nodes.CurvePlotNode import CurvePlotNode
from .nodes.CalcCSNode import CalcCSNode
from .nodes.FreeCodeNone import FreeCodeNode

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
if fw is None:
    app = pg.mkQApp()
    confg.main_fchart = fw = pg.flowchart.Flowchart()

library.addNodeType(    BananaPlotNodeRegion    , [(    'Display'   ,)])
library.addNodeType(    BananaPlotNodeCut       , [(    'Display'   ,)])
library.addNodeType(    BananaPlotNodeCut2      , [(    'Display'   ,)])
library.addNodeType(    BnnSlicesPlotNode       , [(    'Display'   ,)])
library.addNodeType(    CurvePlotNode           , [(    'Display'   ,)])
library.addNodeType(    RegridBnnNode           , [(    'Data'      ,)])
library.addNodeType(    SliceBnnNode            , [(    'Data'      ,)])
library.addNodeType(    DeUtcNode               , [(    'Data'      ,)])
library.addNodeType(    CombineSpectraNode      , [(    'Data'      ,)])
library.addNodeType(    ConcatTimeNode          , [(    'Data'      ,)])
library.addNodeType(    CalcCSNode              , [(    'Calc'      ,)])

library.addNodeType(    PeelNode                , [(    'Peel'      ,)])
library.addNodeType(    GaussianFilterNode      , [(    'Filter'    ,)])
library.addNodeType(    QNormFilterNode         , [(    'Filter'    ,)])
library.addNodeType(    AdaptativeFilterNode    , [(    'Filter'    ,)])
library.addNodeType(    RidgeFilterNode         , [(    'Filter'    ,)])


library.addNodeType(    FileOpenerNode         , [(    'File'       ,)])
library.addNodeType(    FileSaverNode          , [(    'File'       ,)])

library.addNodeType(    CutDpNode              , [(    'Cut'        ,)])
library.addNodeType(    FreeCodeNode           , [(    'Code'       ,)])
# library.addNodeType(    AdaptativeFilterNode    , [(    'Filter'    ,)])

# Add the unsharp mask node to two locations in the menu to demonstrate
# that we can create arbitrary menu structures
# library.addNodeType(UnsharpMaskNode, [('Image',),
#                                       ('Submenu_test','submenu2','submenu3')])

fw.setLibrary(empty)
fw.setLibrary(library)











