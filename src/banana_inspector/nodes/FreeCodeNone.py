# noinspection PyUnresolvedReferences
import numpy as np
# noinspection PyUnresolvedReferences
import pandas as pd
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree

# noinspection PyUnresolvedReferences
from ..util import bnn_array
# from ..util import coag_sink as ucs
# noinspection PyUnresolvedReferences
from .. import util

class FreeCode:
    def __init__(self):
        pass

    # @classmethod
    # def FreeCode(cls, dndldp_cm3, T_k, P_pa):
    #     dN, dp1, dp2 = dndldp_cm3.bnn.get_dN(0, 1)
    #     dN_m3 = dN * 1e6
    #
    #
    #     cs = ucs.calc_CS(
    #         dN_m3,
    #         T=T_k,
    #         P=P_pa
    #     )
    #
    #     return cs




class FreeCodeNode(CtrlNodeTree):
    """calculates the CS from the spectra"""
    nodeName = "FreeCodeNode"
    uiTemplate = [
        {'name'  : 'code',
         'type'  : 'str',
         'value' : 'dataIn',
         },


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

        code = self.ctrls['code']
        dataOut = eval(code)

        return {'dataOut': dataOut}
