import numpy as np
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class QNormFilter():
    def __init__(self):
        pass


    @staticmethod
    def gauss_astro( da_ , xhours , ylog ):

        da0 = da_.transpose('lDp','secs')
        da01 = da0.where(da0>0,0) + 1
        da = np.log10(da01)

        dt = da_['secs'].diff('secs').mean().item()/3600
        dy = da_['lDp'].diff('lDp').mean().item()
        # print(dt)
        # print(dy)

        xpixel = xhours / dt
        ypixel = ylog / dy
        if xpixel == 0:
            xpixel = .0001
        if ypixel == 0:
            ypixel = .0001



        from astropy.convolution import Gaussian2DKernel
        from astropy.convolution import convolve
        kernel = Gaussian2DKernel( x_stddev=xpixel , y_stddev=ypixel )
        res = convolve( da , kernel ,boundary='extend')
        nda = xr.ones_like( da ) * res

        nda1 = 10**nda - 1
        return nda1

    @classmethod
    def norm(cls, da, q0, q1):
        q0_ = da.quantile(q0,dim='secs')
        q1_ = da.quantile(q1,dim='secs')

        d1 = (da/q1_)-(q0_/q1_)

        d2 = 10**d1
        return d2


class QNormFilterNode(CtrlNodeTree):
    """Return the input data passed through an gaussian filter."""
    nodeName = "QNormFilterNode"
    uiTemplate = [
        {
            'name'  : 'q0',
            'type'  : 'float',
            'value' : .05,
            'limits': [0,.5],
            'dec'   : True,
            'step'  : .05
        },
        {
            'name'  : 'q1',
            'type'  : 'float',
            'value' : .95,
            'limits': [.5,1],
            'dec'   : True,
            'step'  : .05
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
            'dataIn' : dict(io='in'),
            'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

    # noinspection PyMethodOverriding
    def process(self, dataIn: xr.DataArray, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        q0 = self.ctrls['q0']
        q1 = self.ctrls['q1']
        dataOut = QNormFilter.norm(
            da=dataIn,
            q0=q0,
            q1=q1)

        return {'dataOut': dataOut}
