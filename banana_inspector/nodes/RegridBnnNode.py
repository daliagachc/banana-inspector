import numpy as np
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class RegridBnn():
    def __init__(self):
        pass

    @staticmethod
    def regrid(*, darray, n_subs, log_dx):
        dx = log_dx / n_subs
        dm = np.ceil(darray['lDp'].min().item() / log_dx) * log_dx
        dM = np.ceil(darray['lDp'].max().item() / log_dx) * log_dx

        dms = np.arange(dm - (((n_subs - 1) / 2) * dx), dM, dx)

        d1 = darray.interp({'lDp': dms})

        dout = d1.coarsen(**{'lDp': n_subs}, boundary='trim').mean().reset_coords(drop=True)

        dout['time'] = dout['secs'].astype('datetime64[s]')

        dout['Dp'] = 10 ** dout['lDp']

        return dout


class RegridBnnNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "RegridBnnNode"
    uiTemplate = [
        {'name': 'n_subs', 'type': 'int', 'value': 11},
        {'name': 'log_dx', 'type': 'float', 'value': .5},
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

        ns = self.ctrls['n_subs']
        dx = self.ctrls['log_dx']

        dataOut = RegridBnn().regrid(darray=dataIn, n_subs=ns, log_dx=dx)

        return {'dataOut': dataOut}
