"""
9/14/21

diego.aliaga at helsinki dot fi
"""
import pyqtgraph_back as pg
from pyqtgraph_back import QtGui

from ..funs import open_darray
# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode


import pyqtgraph_back as pg


KIND = 'Display'



class OpenFileNode(CtrlNode):
    """
    - get the path of a file
    - opens the data for the file
    """
    nodeName = "OpenFileNode"
    uiTemplate = [
        # ('select file: ', 'button',
        #  {
        #      'function': lambda s: print('s'),
        #      'title':'press',
        #
        #
        #  }),

        # ('input file is: ', 'text',
        #  {'value': ''}),

        ('set dir', 'set_dir',
         {
             'value': '',
         }
         ),

        ('set file', 'set_file',
         {
             'value': '',
         }
         ),
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            # 'dirIn': dict(io='in'),
            # each terminal needs at least a name and
            'file_out': dict(io='out'),
            # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNode.__init__(self, name, terminals=terminals)

    def process(self, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {
        # ctrlName: widget}
        # sigma = self.ctrls[ 'sigma' ].value()
        # strength = self.ctrls[ 'strength' ].value()
        # file_path = self.ctrls['input_file'].text()
        # output = dataIn - (
        #             strength * pg.gaussianFilter( dataIn , (sigma , sigma) ))

        # bnn_plot = BananaPlot()
        # dock_area = pg.dockarea
        file_out = self.ctrls['set file'].text()
        # print('input file is', file_path)

        # output = open_darray(file_path)
        return {'file_out': file_out }
