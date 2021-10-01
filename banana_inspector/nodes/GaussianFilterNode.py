"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
import pyqtgraph_back
from pyqtgraph_back import GraphicsLayoutWidget
import pyqtgraph_back as pg
from .. import shared_data
# from ..funs import set_image_data , open_darray

from .. import funs

import pyqtgraph_back.dockarea

from pyqtgraph_back.flowchart import Flowchart , Node
import pyqtgraph_back.flowchart.library as fclib
# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode
from pyqtgraph_back.Qt import QtGui , QtCore
# import pyqtgraph as pg
import numpy as np

class GaussianFilterNode( CtrlNode ):
    """Gaussian smoothing filter."""
    nodeName = 'GaussianFilterNode'
    uiTemplate = [
            ('xsigma' , 'spin' , { 'min': 0.1 , 'max': 100 }),
            ( 'ysigma' , 'spin' , { 'min': 0.1 , 'max': 100 } )
            ]

    def __init__( self , name ):
        ## Define the input / output terminals available on this node
        terminals = {
                'dataIn'  : dict( io='in' ) ,
                # each terminal needs at least a name and
                'dataOut': dict( io='out' ) ,
                # to specify whether it is input or output
                }  # other more advanced options are available
        # as well..
    
        CtrlNode.__init__( self , name , terminals=terminals )
 
    def process( self , dataIn , display=True ):
        xsigma = self.ctrls[ 'xsigma' ].value()
        ysigma = self.ctrls[ 'ysigma' ].value()
        import xarray as xr
        dataIn:xr.Dataset
        data_out = dataIn.copy(deep=True)
        da = data_out['dndlDp']
        res = funs.gauss_astro(da,xsigma,ysigma)
        data_out[ 'dndlDp' ] = res

        return { 'dataOut': data_out }

