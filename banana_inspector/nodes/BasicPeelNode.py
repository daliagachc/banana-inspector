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
from ..pyqtgraph_bnn_extensions import TextEdit


# from ..funs import set_image_data , open_darray


class BnnPeelROI(pg.PolyLineROI):
    def __init__(self, view_positions=None, pos=None):
        # print( args )
        if view_positions is None:
            view_positions = []
        pg.PolyLineROI.__init__(
            self, view_positions, pos=pos, removable=True,
            closed=True)

    def add_point(self, view_xy):
        xys = self.get_roi_pol_coords()
        xys.append(view_xy)
        xys_kid = [self.mapFromParent(xy) for xy in xys]

        # todo there is an error heere with remove item
        self.setPoints(xys_kid)

    def get_roi_pol_coords(self):
        """gets the ROI list of coords in the axis mapping"""
        pts = self.getState()['points']
        pts = [self.mapToParent(p) for p in pts]

        return pts

    def pol_coords_to_str(self):
        pts = self.get_roi_pol_coords()
        sts = [f'[{p.x():.4f}\t,{p.y():.4f}\t],\n' for p in pts]
        st = ''.join(sts)
        s1 = f'[\n{st}]'
        return s1

    def get_mouse_clicked_fun(self, plot_item, ):
        def mouseClicked(evt):
            # print('c')
            mc = evt[
                0]  ## using signal proxy turns original arguments into
            # a tuple
            if not mc.double():
                return

            pos = mc.scenePos()
            viewPoint = plot_item.vb.mapSceneToView(pos)
            self.add_point(viewPoint)

        return mouseClicked

    @staticmethod
    def get_the_proxi(plot_item, mouseClicked):
        proxy = pg.SignalProxy(plot_item.scene().sigMouseClicked,
                               rateLimit=60, slot=mouseClicked)
        return proxy


class BasicPeelNode(CtrlNode):
    """Gaussian smoothing filter."""
    nodeName = 'BasicPeelNode'
    uiTemplate = [
        # ('xsigma', 'doubleSpin', {'min': 0, 'max': 1000000}),
        # ('ysigma', 'doubleSpin', {'min': 0, 'max': 1000000})
        ('points', 'peel_edit', {'text': '[[]]'})
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
        self.peel_roi: BnnPeelROI = None
        self.bnn_plot = None
        self.proxi = None

        self.ctrl_points: TextEdit = self.ctrls['points']

        self.ctrl_points.editingFinished.connect(self.ctrl_text_changed)

        self.reset_create_roi()

    def reset_create_roi(self, **kwargs):
        if self.peel_roi is not None:
            print('remove roi implement')

        self.peel_roi = BnnPeelROI(**kwargs)

        self.peel_roi.sigRegionChangeFinished.connect(self.roi_changed)

    def ctrl_text_changed(self):
        print('ctrl_text_changed')
        text = self.ctrl_points.toPlainText()
        t1 = text.replace(' ','')
        if t1 == '':
            t1 = '[]'

        t2 = self.peel_roi.pol_coords_to_str()
        if t1 != t2:
            pts = eval(t1)

            p1 = [self.peel_roi.mapFromParent(pg.QtCore.QPointF(*xy)) for xy in pts]

            self.peel_roi.setPoints(p1)



    def roi_changed(self):
        print('roi changed')
        txt = self.peel_roi.pol_coords_to_str()
        txt1 = self.ctrl_points.toPlainText()
        if txt!=txt1:
            self.ctrl_points.setText(txt)

            # todo fix the emit recursie so that we can save directly
            print('we are really emitting now')
            self.ctrl_points.editingFinished.emit()
        pass

    def process(self, data_array, banana_plot: BananaPlot, display=True):
        # todo do we need something form this function?
        # self.probably_remove_this(banana_plot)

        # xsigma = self.ctrls[ 'xsigma' ].value()
        # ysigma = self.ctrls[ 'ysigma' ].value()
        # import xarray as xr
        # dataIn:xr.Dataset
        data_out = data_array.copy(deep=True)
        # da = data_out['dndlDp']
        # res = funs.gauss_astro(da,xsigma,ysigma)
        # data_out[ 'dndlDp' ] = res

        # if self.peel_roi is None:
        #     p1 = banana_plot.plot_item
        #     r = p1.viewRange()
        #     x = np.mean(r[0])
        #     y = np.mean(r[1])
        #
        #     self.peel_roi = BnnPeelROI(pos=[x, y])
        #     p1.addItem(self.peel_roi)
        #
        #
        #
        #     proxy2 = pg.SignalProxy(p1.scene().sigMouseClicked,
        #                             rateLimit=60, slot=mouseClicked)
        # data_out = self.peel_roi.get_roi_pol_coords()
        # print('process', proxy2)

        return {'peel_points': data_out}

    def probably_remove_this(self, banana_plot):
        if self.peel_roi is not None:
            print('deleting')
            if self.bnn_plot is not None:
                self.bnn_plot.plot_item.removeItem(self.peel_roi)
                print('del again')

                # self.peel_roi = None
        self.bnn_plot = banana_plot
        if self.bnn_plot:
            print('not none')
            p1 = self.bnn_plot.plot_item
            r = p1.viewRange()
            x = np.mean(r[0])
            y = np.mean(r[1])
            if x != 0:
                self.reset_create_roi(pos=[x, y])
                # self.peel_roi = BnnPeelROI(pos=[x, y])
                p1.addItem(self.peel_roi)
                fun = self.peel_roi.get_mouse_clicked_fun(p1)
                self.proxi = self.peel_roi.get_the_proxi(p1, fun)
