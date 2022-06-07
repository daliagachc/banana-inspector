import numpy as np
import pandas as pd
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class CutDp:
    def __init__(self):
        pass

    @classmethod
    def cut_Dp(cls, dataIn, lDp_min, lDp_max):
        return dataIn.loc[{'lDp':slice(lDp_min,lDp_max)}]


class CutDpNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "CutDpNode"
    uiTemplate = [
        {'name'  : 'lDp_min',
         'type'  : 'float',
         'value' : -9,
         'limits': [-9, -6],
         'step'  : .1
         },

        {'name'  : 'lDp_max',
         'type'  : 'float',
         'value' : -6,
         'limits': [-9, -6],
         'step'  : .1
         }

        # {'name': 'log_dx', 'type': 'float', 'value': .5},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        # {'name': 'dock', 'type': 'str', 'value': 'BnnPlotCut'}
        # {'name': 'dock', 'type': 'str', 'value': 'BnnSlicesDock'}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

    # noinspection PyMethodOverriding
    def process(self,
                dataIn:xr.DataArray,
                display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        lDp_min = self.ctrls['lDp_min']
        lDp_max = self.ctrls['lDp_max']

        # dim = 'lDp'

        dataOut = CutDp.cut_Dp(dataIn=dataIn,lDp_min=lDp_min,lDp_max=lDp_max)
        return {'dataOut': dataOut}
