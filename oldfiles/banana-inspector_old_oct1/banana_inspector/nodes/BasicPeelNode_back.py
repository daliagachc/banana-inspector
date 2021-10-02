"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
# import pyqtgraph as pg
import numpy as np
import pyqtgraph_back as pg

from banana_inspector.plotters.BananaPlot import BananaPlot
# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode


# from ..funs import set_image_data , open_darray


def get_mouse_clicked_fun(plot_item, peel_roi):
    def mouseClicked(evt):
        # print('c')
        mc = evt[
            0]  ## using signal proxy turns original arguments into
        # a tuple
        if not mc.double():
            return

        pos = mc.scenePos()
        viewPoint = plot_item.vb.mapSceneToView(pos)
        peel_roi.add_view_point(viewPoint)

    return mouseClicked

def get_the_proxi(plot_item, mouseClicked):
    proxy2 = pg.SignalProxy(plot_item.scene().sigMouseClicked,
                            rateLimit=60, slot=mouseClicked)
    return proxy2


class BnnPeelROI(pg.PolyLineROI):
    def __init__(self, view_positions=None, pos=None):
        # print( args )
        if view_positions is None:
            view_positions = []
        pg.PolyLineROI.__init__(
            self, view_positions, pos=pos,
            closed=True)

    def add_point(self, view_xy):
        xys = self.get_roi_pol_coords()
        xys.append(view_xy)
        xys_kid = [self.mapFromParent(xy) for xy in xys]

        self.setPoints(xys_kid)

    def get_roi_pol_coords(self):
        """gets the ROI list of coords in the axis mapping"""
        pts = self.getState()['points']
        pts = [self.mapToParent(p) for p in pts]

        return pts


class BasicPeelNode(CtrlNode):
    """Gaussian smoothing filter."""
    nodeName = 'BasicPeelNode'
    uiTemplate = [
        ('xsigma', 'doubleSpin', {'min': 0, 'max': 1000000}),
        ('ysigma', 'doubleSpin', {'min': 0, 'max': 1000000})
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'data_array': dict(io='in'),
            'banana_plot': dict(io='in'),
            # each terminal needs at least a name and
            'peel_points': dict(io='out'),
            # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNode.__init__(self, name, terminals=terminals)
        self.peel_roi = None

    def process(self, data_array, banana_plot: BananaPlot, display=True):
        # xsigma = self.ctrls[ 'xsigma' ].value()
        # ysigma = self.ctrls[ 'ysigma' ].value()
        # import xarray as xr
        # dataIn:xr.Dataset
        data_out = data_array.copy(deep=True)
        # da = data_out['dndlDp']
        # res = funs.gauss_astro(da,xsigma,ysigma)
        # data_out[ 'dndlDp' ] = res

        if self.peel_roi is None:
            p1 = banana_plot.plot_item
            r = p1.viewRange()
            x = np.mean(r[0])
            y = np.mean(r[1])

            self.peel_roi = BnnPeelROI(pos=[x, y])
            p1.addItem(self.peel_roi)

            def mouseClicked(evt):
                print('c')
                mc = evt[
                    0]  ## using signal proxy turns original arguments into
                # a tuple
                if not mc.double():
                    return

                pos = mc.scenePos()
                viewPoint = p1.vb.mapSceneToView(pos)
                self.peel_roi.add_view_point(viewPoint)

            proxy2 = pg.SignalProxy(p1.scene().sigMouseClicked,
                                    rateLimit=60, slot=mouseClicked)
        data_out = self.peel_roi.get_roi_pol_coords()
        print('process', proxy2)

        return {'peel_points': data_out}
