import numpy as np
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree

class DeUtc():
    def __init__(self):
        pass


class DeUtcNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "DeUtcNode"
    uiTemplate = [
        {'name': 'hours', 'type': 'int', 'value': -4},
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
    def process(self, dataIn: xr.DataArray, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        h = self.ctrls['hours']
        secs = h * 3600

        dataOut = dataIn.copy(deep=True)
        dataOut['secs'] = dataOut['secs'] + secs

        dataOut['time'] = dataOut['secs'].astype('datetime64[s]')


        return {'dataOut': dataOut}
