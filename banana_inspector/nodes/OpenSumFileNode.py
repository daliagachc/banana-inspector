"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
import pyqtgraph
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
from .. import shared_data
# from ..funs import set_image_data , open_darray

from .. import funs

import pyqtgraph.dockarea

from pyqtgraph.flowchart import Flowchart , Node
import pyqtgraph.flowchart.library as fclib
# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode
from pyqtgraph.Qt import QtGui , QtCore
# import pyqtgraph as pg
import numpy as np

class OpenSumFileNode( CtrlNode ):
    """
    - get the path of a file
    - opens the data for the file
    """
    nodeName = "OpenSumFileNode"
    uiTemplate = [
            ('input_file' , 'text' ,
             { 'value': '' })
            ]
    
    def __init__( self , name ):
        ## Define the input / output terminals available on this node
        terminals = {
                'dirIn' : dict( io='in' ) ,
                # each terminal needs at least a name and
                'dataOut': dict( io='out' ) ,
                # to specify whether it is input or output
                }  # other more advanced options are available
        # as well..
        
        CtrlNode.__init__( self , name , terminals=terminals )
        
    def process( self , dirIn , display=True ):
        # CtrlNode has created self.ctrls, which is a dict containing {
        # ctrlName: widget}
        # sigma = self.ctrls[ 'sigma' ].value()
        # strength = self.ctrls[ 'strength' ].value()
        file_path = self.ctrls['input_file'].text()
        # output = dataIn - (
        #             strength * pg.gaussianFilter( dataIn , (sigma , sigma) ))
        
        # bnn_plot = BananaPlot()
        # dock_area = pg.dockarea
        print( 'input file is', file_path)
        
        # output = open_darray(file_path)
        
        output = funs.open_sum(file_path)
        return { 'dataOut': output }
