import xarray as xr
from skimage import exposure

from .CtrlNodeTree import CtrlNodeTree


class AdaptativeFilter:
    def __init__(self):
        pass

    @staticmethod
    def filter(da_, clip_limit, kx,ky):
        da0:xr.DataArray = da_.transpose('lDp', 'secs').copy(deep=True)
        # da01 = da0.where(da0>0,0) + 1

        vmax = da0.quantile(.999).item()

        da1 = da0/vmax
        da2 = da1.where(da1<1,1)

        img = da2.values

        img1 = exposure.equalize_adapthist(img, kernel_size = [kx,ky], clip_limit=clip_limit)

        nda1 = da0 * 0 + img1
        return nda1


class AdaptativeFilterNode(CtrlNodeTree):
    """Return the input data passed through an adaptative equal histogram filter
    https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_equalize.html#sphx-glr-auto-examples-color-exposure-plot-equalize-py"""
    nodeName = "AdaptativeFilterNode"
    uiTemplate = [
        {
            'name'  : 'clip_limit',
            'type'  : 'float',
            'value' : 0.03,
            'limits': [0.000, 20],
            'dec'   : True,
            'step'  : .005
        },
        {
            'name'  : 'kx',
            'type'  : 'int',
            'value' : 6,
            'limits': [0.000, 2000],
            'dec'   : True,
            'step'  : .1
        },
        {
            'name'  : 'ky',
            'type'  : 'int',
            'value' : 0,
            'limits': [0.000, 2000],
            'dec'   : True,
            'step'  : .1
        },

        # {
        #     'name'  : 'y_log',
        #     'type'  : 'float',
        #     'value' : .01,
        #     'limits': [0.001, 1],
        #     'dec'   : True,
        #     'step'  : .01
        # },
        # {'name': 'log_dx', 'type': 'float', 'value': .5},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        # {'name': 'dock', 'type': 'str', 'value': 'BnnPlotCut'}
        # {'name': 'dock', 'type': 'str', 'value': 'BnnSlicesDock'}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn' : dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

    # noinspection PyMethodOverriding
    def process(self, dataIn: xr.DataArray, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        clip_limit = self.ctrls['clip_limit']
        kx = self.ctrls['kx']
        ky = self.ctrls['ky']


        dataOut = AdaptativeFilter.filter(
            da_=dataIn,
            clip_limit=clip_limit,
            kx=kx,
            ky=ky,
        )

        return {'dataOut': dataOut}
