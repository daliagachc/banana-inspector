"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
# from ..funs import set_image_data , open_darray

from .. import funs

# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode


# import pyqtgraph as pg

KIND = 'Data'

class OpenSumFileNode(CtrlNode):
    """

    - opens the data for the file
    """
    nodeName = "OpenSumFileNode"
    uiTemplate = [
        # ('input_file', 'text',
        #  {'value': ''})
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'path_in': dict(io='in'),
            # each terminal needs at least a name and
            'data_out': dict(io='out'),
            # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, path_in=None, display=True):
        if path_in:


            data_out = funs.open_sum(path_in)
        else:
            data_out = None
        return {'data_out': data_out}
