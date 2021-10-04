"""
9/14/21
this is a barebones sum files representation in xarray
diego.aliaga at helsinki dot fi
"""
# import pyqtgraph as pg
import numpy as np
import pyqtgraph as pg
import pyqtgraph.dockarea
from .CtrlNodeTree import CtrlNodeTree
from .. import confg
from .BananaPlotNodeCut import BananaPlotCut
from .BananaPlotNodeCut import BananaPlotNodeCut


# from pyqtgraph.flowchart.library.common import CtrlNode
# from ..pyqtgraph_bnn_extensions import CtrlNodeExt as CtrlNode
# from ..pyqtgraph_bnn_extensions import PlainTextEdit

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


class PeelNode(CtrlNodeTree):
    """draw the region around the banana event so that the GR can be easily calculated"""
    nodeName = 'PeelNode'
    uiTemplate = [
        {'name': 'dock',
        'type': 'str',
        'value': nodeName},

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

        {'name'  : 'points',
         'type'  : 'text',
         # 'value' : 1,
         # 'limits': [0, 1e5],
         # 'step'  : .1,
         # 'dec'   : True,
         },
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'peel_points': dict(io='out'),
            'peel_roi'   : dict(io='out'),
            'dataIn': dict(io='in'),
            't1'    : dict(io='in'),
            't2'    : dict(io='in'),
            # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.peel_roi: BnnPeelROI2 = BnnPeelROI2()
        self.bnn_plot = None
        self.proxi = None

        self.dock = None
        # noinspection PyTypeChecker
        self.bp: BananaPlotCut = None

        self.ctrl_points = self.ctrls['points']

        # self.ctrl_points.textChanged.connect(self.ctrl_text_changed)
        self.ctrls.sigTreeStateChanged.connect(self.ctrl_text_changed)

        self.peel_roi.sigRegionChangeFinished.connect(self.roi_changed)

        self.roi_painted = False

        # self.reset_create_roi()

    def _del_reset_create_roi(self, **kwargs):
        if self.peel_roi is not None:
            print('remove roi implement')

        self.peel_roi = BnnPeelROI2(**kwargs)

        self.peel_roi.sigRegionChangeFinished.connect(self.roi_changed)

    def ctrl_text_changed(self):
        print('ctrl_text_changed')
        text = self.ctrl_points
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
        txt1 = self.ctrl_points
        if txt != txt1:
            self.ctrl_points = txt

            # todo fix the emit recursie so that we can save directly
            print('we are really emitting now')

        pass
    def process(self, dataIn, t1, t2, display=True):

        dock_area = confg.dock_area
        duck_name = self.ctrls['dock'] = self.name()

        if duck_name not in dock_area.findAll()[1].keys():
            bp = BananaPlotCut(None)
            dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
            dock.addWidget(bp)
            dock_area.addDock(dock)
            confg.connectMasterXY(bp.plot_item, confg.par_tree)

            self.dock = dock
            self.bp = bp

        self.bp.set_image_data_cut(dataIn, t1, t2)
        # self.bp.set_region_ui(dataIn, t1, t2)

        self.bp.set_hist_levels(da=dataIn)
        self.bp.plot_item.enableAutoRange(axis='x', enable=True)

        self.blockSignals(False)



        st = self.ctrls['points']
        data_out = eval(st)

        if self.roi_painted is False:
            self.peel_roi.draw_me_in_plot(self.bp.plot_item)
            self.roi_painted = True



        return {
            'peel_points': data_out,
            'peel_roi'   : self.peel_roi
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
