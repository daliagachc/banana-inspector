import xarray as xr
from skimage.filters import frangi

from .CtrlNodeTree import CtrlNodeTree


# from skimage import exposure


class RidgeFilter:
    def __init__(self):
        pass

    @staticmethod
    def filter(da_,
               alpha,
               beta,
               gamma,
               sm,
               sM,
               sS
               ):
        da0 = da_.transpose('lDp', 'secs').copy(deep=True)
        # da01 = da0.where(da0>0,0) + 1

        img = da0.values

        img1 = frangi(
            img,
            # sigmas=[1],
            scale_range=[sm,sM],
            scale_step=sS,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            black_ridges=False,
            mode='nearest',
            cval=0,
        )

        # img1 = exposure.equalize_adapthist(img, clip_limit=clip_limit)

        nda1 = da0 * 0 + img1
        return nda1


class RidgeFilterNode(CtrlNodeTree):
    """
    Return the input data passed through an ridge filter
    https://scikit-image.org/docs/stable/auto_examples/edges/plot_ridge_filter.html#sphx-glr-auto-examples-edges-plot-ridge-filter-py
    """

    nodeName = "RidgeFilterNode"
    uiTemplate = [
        {
            'name'  : 'alpha',
            'type'  : 'float',
            'value' : 0.5,
            'limits': [0.0000, 100],
            'dec'   : True,
            'step'  : .1
        },
        {
            'name'  : 'beta',
            'type'  : 'float',
            'value' : 0.5,
            'limits': [0.0000, 100],
            'dec'   : True,
            'step'  : .1
        },
        {
            'name'  : 'gamma',
            'type'  : 'float',
            'value' : 0.00001,
            'limits': [0.0000, 200],
            'dec'   : True,
            'step'  : .001
        },

        {
            'name'  : 'sm',
            'type'  : 'float',
            'value' : 1,
            'limits': [0.0000, 200],
            'dec'   : True,
            'step'  : 1
        },

        {
            'name'  : 'sM',
            'type'  : 'float',
            'value' : 10,
            'limits': [0.0000, 200],
            'dec'   : True,
            'step'  : 1
        },

        {
            'name'  : 'sS',
            'type'  : 'float',
            'value' : 2,
            'limits': [0.0000, 200],
            'dec'   : True,
            'step'  : 1
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

        # clip_limit = self.ctrls['clip_limit']
        alpha = self.ctrls['alpha']
        beta = self.ctrls['beta']
        gamma = self.ctrls['gamma']
        sm = self.ctrls['sm']
        sM = self.ctrls['sM']
        sS = self.ctrls['sS']

        dataOut = RidgeFilter.filter(
            da_=dataIn,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            sm=sm,
            sM = sM,
            sS = sS,

        )

        return {'dataOut': dataOut}
