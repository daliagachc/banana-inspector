import numpy as np
import pandas as pd
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class CombineSpectra:
    def __init__(self):
        pass

    @staticmethod
    def is_regular_grid(coor, tolerance_percentage=1):
        from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks

        tol = tolerance_percentage / 100

        bks = infer_interval_breaks(coor, check_monotonic=True)

        d = pd.Series(bks).diff()

        n = d / np.mean(d)
        m = np.abs(n - 1)

        bo = (m > tol).sum() == 0

        #     print(tol)

        return bo

    @staticmethod
    def combine_2_spectras(
            darray_min,
            darray_max,
            cut_dim,
            cut_point

    ):
        y1 = cut_point
        cor = cut_dim

        is_regular_grid = CombineSpectra.is_regular_grid

        assert is_regular_grid(darray_min['lDp'])
        assert is_regular_grid(darray_max['lDp'])
        assert is_regular_grid(darray_min['secs'])
        assert is_regular_grid(darray_max['secs'])

        assert (darray_min['secs'] - darray_max['secs']).sum().item() == 0

        d11 = darray_min.loc[{cor: slice(None, y1)}]
        d22 = darray_max.loc[{cor: slice(y1, None)}]

        first = d22[cor].min().item()

        last = d11[cor].max().item()

        dx = d11[cor].to_series().diff().mean()

        dis = np.abs((first - (last)) / dx)

        if dis < .01:
            d11 = d11[{cor: slice(None, -1)}]

        d3 = xr.concat([d11, d22], cor)

        # return d3,d22,d11

        assert is_regular_grid(d3['lDp'])
        assert is_regular_grid(d3['secs'])

        return d3


class CombineSpectraNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "CombineSpectraNode"
    uiTemplate = [
        {'name'  : 'lDp_cut',
         'type'  : 'float',
         'value' : -8,
         'limits': [-10, -2],
         'step'  : .1},

        {'name'  : 'magL',
         'type'  : 'float',
         'value' : 1,
         'limits': [0, 1e5],
         'step'  : .1,
         'dec'   : True
         },

        {'name'  : 'magU',
         'type'  : 'float',
         'value' : 1,
         'limits': [0, 1e5],
         'step'  : .1,
         'dec'   : True,
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
            'dataLow': dict(io='in'),
            'dataUp' : dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

    # noinspection PyMethodOverriding
    def process(self,
                dataLow: xr.DataArray,
                dataUp: xr.DataArray,
                display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        lDp_cut = self.ctrls['lDp_cut']

        dim = 'lDp'

        dL = dataLow * self.ctrls['magL']
        dU = dataUp * self.ctrls['magU']
        dataOut = CombineSpectra.combine_2_spectras(
            darray_min=dL,
            darray_max=dU,
            cut_dim=dim,
            cut_point=lDp_cut)

        return {'dataOut': dataOut}
