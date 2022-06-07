import xarray as xr

from .CtrlNodeTree import CtrlNodeTree


class QNormFilter():
    def __init__(self):
        pass

    @classmethod
    def norm(cls, da, xlen
             # q0, q1
             ):
        # q0_ = da.quantile(q0,dim='secs')
        # q1_ = da.quantile(q1,dim='secs')
        r = da.rolling(secs=xlen, min_periods=1, center=True)
        rM = r.max()
        rm = r.min()
        dd1 = (da - rm) / (rM - rm)

        # d1 = (da-q0_)/(q1_-q0_)
        # d2 = 10**d1

        return dd1
    @classmethod
    def norm1(cls, da, xlen
             # q0, q1
             ):
        # q0_ = da.quantile(q0,dim='secs')
        # q1_ = da.quantile(q1,dim='secs')
        r = da.rolling(secs=xlen, min_periods=1, center=True)
        rM = r.max()
        rm = r.min()
        dd1 = (da - rm) / (rM - rm)

        # d1 = (da-q0_)/(q1_-q0_)
        # d2 = 10**d1

        return dd1

class QNormFilterNode(CtrlNodeTree):
    """Return the input data passed through an gaussian filter."""
    nodeName = "QNormFilterNode"
    uiTemplate = [
        {
            'name'  : 'xlen',
            'type'  : 'int',
            'value' : 13,
            'limits': [1, 100],
            'dec'   : True,
            'step'  : 1
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

        # q0 = self.ctrls['q0']
        # q1 = self.ctrls['q1']
        xlen = self.ctrls['xlen']
        dataOut = QNormFilter.norm(
            da=dataIn,
            xlen=xlen
            # q0=q0,
            # q1=q1
        )

        return {'dataOut': dataOut}
