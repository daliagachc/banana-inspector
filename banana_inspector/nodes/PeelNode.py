"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
# import pyqtgraph as pg
import numpy as np
import pyqtgraph_back as pg

# from pyqtgraph.flowchart.library.common import CtrlNode
from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode
from ..pyqtgraph_bnn_extensions import PlainTextEdit


# from ..funs import set_image_data , open_darray


class BnnPeelROI2(pg.PolyLineROI):
    def __init__(self, view_positions=None):
        # print( args )
        if view_positions is None:
            view_positions = []

        pg.PolyLineROI.__init__(
            self, positions=view_positions, removable=True,
            closed=True)
        self.plot_item: pg.PlotItem = None

    def add_view_point(self, view_xy):
        xys = self.get_roi_view_coords()
        xys.append(view_xy)
        xys_kid = [self.mapFromParent(xy) for xy in xys]

        # todo there is an error heere with remove item
        self.blockSignals(True)
        self.setPoints(xys_kid)
        self.blockSignals(False)
        self.sigRegionChangeFinished.emit(self)

    def get_roi_view_coords(self):
        """gets the ROI list of coords in the axis mapping"""
        pts = self.getState()['points']
        if pts:
            pts = [self.mapToParent(p) for p in pts]

        return pts

    def get_roi_view_coords_to_str(self):
        pts = self.get_roi_view_coords()
        if pts:
            sts = [f'[{p.x():.4f}\t,{p.y():.4f}\t],\n' for p in pts]
            st = ''.join(sts)
            s1 = f'[\n{st}]'
        else:
            s1 = '[]'
        return s1

    def get_mouse_clicked_fun(self, plot_item, ):
        def mouseClicked(evt):
            # print('c')
            mc = evt[0]
            ## using signal proxy turns original arguments into
            # a tuple
            if not mc.double():
                return

            pos = mc.scenePos()
            viewPoint = plot_item.vb.mapSceneToView(pos)
            self.add_view_point(viewPoint)

        return mouseClicked

    @staticmethod
    def get_the_proxi(plot_item, mouseClicked):
        proxy = pg.SignalProxy(plot_item.scene().sigMouseClicked,
                               rateLimit=60, slot=mouseClicked)
        return proxy

    def draw_me_in_plot(self, new_plot: pg.PlotItem):
        dif = id(self.plot_item) != id(new_plot)
        if dif:
            self._remove_me_from_plot()
            self._add_me_to_new_plot(new_plot)

            ### add click interaction
            self.fun = self.get_mouse_clicked_fun(new_plot)
            self.proxi = self.get_the_proxi(new_plot, self.fun)

    def _remove_me_from_plot(self):
        if self.plot_item:
            self.plot_item.removeItem(self)
            self.plot_item = None

    def _add_me_to_new_plot(self, new_plot: pg.PlotItem):
        assert self.plot_item is None
        new_plot.addItem(self)
        self.plot_item = new_plot


class PeelNode(CtrlNode):
    """Gaussian smoothing filter."""
    nodeName = 'PeelNode'
    uiTemplate = [
        # ('xsigma', 'doubleSpin', {'min': 0, 'max': 1000000}),
        ('ysigma', 'doubleSpin', {'min': 0, 'max': 1000000}),
        # todo implement this
        ('points', 'multi_text', {'text': '[]'})
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'peel_points': dict(io='out'),
            'peel_roi': dict(io='out')
            # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNode.__init__(self, name, terminals=terminals)
        self.peel_roi: BnnPeelROI2 = BnnPeelROI2()
        self.bnn_plot = None
        self.proxi = None

        self.ctrl_points: PlainTextEdit = self.ctrls['points']

        self.ctrl_points.textChanged.connect(self.ctrl_text_changed)
        self.peel_roi.sigRegionChangeFinished.connect(self.roi_changed)

        # self.reset_create_roi()

    def _del_reset_create_roi(self, **kwargs):
        if self.peel_roi is not None:
            print('remove roi implement')

        self.peel_roi = BnnPeelROI(**kwargs)

        self.peel_roi.sigRegionChangeFinished.connect(self.roi_changed)

    def ctrl_text_changed(self):
        print('ctrl_text_changed')
        text = self.ctrl_points.toPlainText()
        t1 = text.replace(' ', '')
        if t1 == '':
            t1 = '[]'

        t2 = self.peel_roi.get_roi_view_coords_to_str()
        if t1 != t2:
            try:
                pts = eval(t1)
            except SyntaxError:
                print('bad syntax, setting back to t2')
                self.ctrl_points.setPlainText(t2)
                return

            p1 = [self.peel_roi.mapFromParent(pg.QtCore.QPointF(*xy)) for xy in pts]

            self.peel_roi.setPoints(p1)

    def roi_changed(self):
        print('roi changed')
        txt = self.peel_roi.get_roi_view_coords_to_str()
        txt1 = self.ctrl_points.toPlainText()
        if txt != txt1:
            self.ctrl_points.setPlainText(txt)

            # todo fix the emit recursie so that we can save directly
            print('we are really emitting now')

        pass

    def process(self, In=None,
                # data_array=None,
                # banana_plot=None,
                # BananaPlot=None,
                display=True
                ):
        s = self.stateGroup.state()
        st = self.ctrls['points'].toPlainText()
        data_out = eval(st)

        print('starting process peel node')

        # todo do we need something form this function?
        # self.probably_remove_this(banana_plot)

        # xsigma = self.ctrls[ 'xsigma' ].value()
        # ysigma = self.ctrls[ 'ysigma' ].value()
        # import xarray as xr
        # dataIn:xr.Dataset
        # data_out = data_array.copy(deep=True)
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

        return {
            'peel_points': data_out,
            'peel_roi': self.peel_roi
        }


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
