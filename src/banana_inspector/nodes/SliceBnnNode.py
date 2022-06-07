import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class SliceBnnNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "SliceBnnNode"
    uiTemplate = [
        # {'name': 't1', 'type': 'float', 'value': 1e9},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        # {'name': 'dock', 'type': 'str', 'value': 'BnnPlotCut'}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            'dataOut': dict(io='out'),
            't1': dict(io='in'),
            't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        # self.dock = None
        # self.bp = None

    # noinspection PyMethodOverriding
    def process(self, dataIn: xr.DataArray, t1, t2, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        dataOut = dataIn.loc[{'secs': slice(t1, t2)}]

        return {'dataOut':dataOut}
