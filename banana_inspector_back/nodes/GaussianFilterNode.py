import numpy as np
import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class GaussianFilter():
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


class GaussianFilterNode(CtrlNodeTree):
    """Return the input data passed through an gaussian filter."""
    nodeName = "GaussianFilterNode"
    uiTemplate = [
        {
            'name'  : 'x_h',
            'type'  : 'float',
            'value' : .01,
            'limits': [0.0001,2],
            'dec'   : True,
            'step'  : .1
        },
        {
            'name'  : 'y_log',
            'type'  : 'float',
            'value' : .01,
            'limits': [0.001,1],
            'dec'   : True,
            'step'  : .01
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

        x_h = self.ctrls['x_h']
        y_log = self.ctrls['y_log']

        dataOut = GaussianFilter.gauss_astro(
            da_=dataIn,
            xhours=x_h,
            ylog=y_log)

        return {'dataOut': dataOut}
