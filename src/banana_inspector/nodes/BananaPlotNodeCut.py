import numpy as np
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph import LinearRegionItem
from pyqtgraph.Qt import QtCore
from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks

from .CtrlNodeTree import CtrlNodeTree
from .. import confg


class BananaPlotCut(pg.GraphicsLayoutWidget):

    def __init__(self, parent, **kargs):
        super().__init__(parent=parent, **kargs)

        # self.time_axis = pg.DateAxisItem( utcOffset=0 )

        axisItems = {'bottom': pg.DateAxisItem(utcOffset=0)}
        plot_item: pg.PlotItem = pg.PlotItem(axisItems=axisItems)

        plot_item.setTitle("log( dN /dlog(Dp) )")
        # plot_item.setAxisItems()
        plot_item.setLogMode(x=None, y=True)

        image_item = pg.ImageItem()
        plot_item.addItem(image_item)

        hist = pg.HistogramLUTItem()
        hist.axis.setLogMode(True)
        hist.gradient.loadPreset('viridis')
        hist.setImageItem(image_item)

        # Isocurve drawing
        iso = pg.IsocurveItem(level=0.8, pen='g')
        iso.setParentItem(image_item)
        iso.setZValue(5)

        # Draggable line for setting isocurve level
        isoLine = pg.InfiniteLine(angle=0, movable=True, pen='g')
        hist.vb.addItem(isoLine)
        hist.vb.setMouseEnabled(y=False)  # makes user interaction a little easier
        isoLine.setValue(2)
        isoLine.setZValue(1000)  # bring iso line above contrast controls

        plot_item.setXLink(confg.dummy_plot_item_1)

        def updateIsocurve():
            iso.setLevel(isoLine.value())

        isoLine.sigDragged.connect(updateIsocurve)

        self.ci.addItem(hist)
        self.ci.addItem(plot_item)

        self.image_item = image_item
        self.plot_item:pg.PlotItem = plot_item

        # noinspection PyTypeChecker
        self.region: LinearRegionItem = None
        self.proxi = None
        self.hist = hist
        self.image_item = image_item
        self.iso = iso
        self.isoLine = isoLine

    def set_image_data(self, da, autoLevels, log10, iso):
        d2 = self.check_transpose(da)
        self._set_image_data(d2,
                             autoLevels=autoLevels,
                             log10=log10,
                             iso=iso
                             )

    def set_hist_levels(self, da):
        dn = da.where(da > 0)
        m, M = dn.quantile([.15, .99])
        mm = np.log10(m.item())
        MM = np.log10(M.item())
        self.hist.setLevels(mm, MM)

    def set_region_ui(self, da, t1=None, t2=None):
        vb = self.plot_item.vb
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot_item.addItem(vLine, ignoreBounds=True)
        self.plot_item.addItem(hLine, ignoreBounds=True)
        label = pg.LabelItem(justify='right')
        label.setText('')
        # noinspection PyArgumentList
        self.addItem(label, row=1, col=1)

        def mouseMoved(evt):
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.plot_item.sceneBoundingRect().contains(pos):
                mousePoint = vb.mapSceneToView(pos)

                date = pd.to_datetime(mousePoint.x() * 1e9).strftime('%Y-%m-%d %H:%M')
                label.setText(f'{date}|{10 ** mousePoint.y() * 1e9:3.2f} nm')
                #         if index > 0 and index < len(data1):
                #             label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
                vLine.setPos(mousePoint.x())
                hLine.setPos(mousePoint.y())

        self.proxy = pg.SignalProxy(self.plot_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

        t1_, t2_ = da['secs'][{'secs': [0, -1]}].values

        tmm = (t1_ + t2_) / 2

        t1o = tmm - 3600 * 24
        t2o = tmm + 3600 * 24

        if t1:
            if t1 > t1_:
                t1o = t1
        if t1:
            if t2 < t2_:
                t2o = t2

        region = pg.LinearRegionItem(values=(t1o, t2o))
        region.setZValue(10)

        self.region = region
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.plot_item.addItem(region, ignoreBounds=True)

    def set_image_data_cut(self, da, t1, t2, log10, auto_range, iso):
        d_cut = da.loc[{'secs': slice(t1, t2)}]
        d2 = self.check_transpose(d_cut)
        self._set_image_data(d2, auto_range, log10, iso)

    @staticmethod
    def check_transpose(da: xr.DataArray):
        order = ('secs', 'lDp')
        if da.dims != order:
            da1 = da.transpose(*order)
        else:
            da1 = da
        return da1

    def _set_image_data(self, da, autoLevels, log10, iso):
        img: pg.ImageItem = self.image_item
        d0, d1, t00, t11 = get_darray_bounds(da)
        if log10:
            da1 = da.where(da > 1, 1)
            lda = np.log10(da1)
        else:
            lda = da
            self.hist.axis.setLogMode(False)
        # lda = lda.where(lda>0,0)
        data = lda.values
        img.setImage(data, autoLevels=autoLevels)
        width = t11 - t00
        height = d1 - d0
        rect = QtCore.QRectF(t00, d0, width, height)
        img.setRect(rect)
        if iso:
            self.iso.setData(data)


def to_sec(date):
    s1 = date - np.datetime64(0, 'Y')
    s2 = s1 / np.timedelta64(1, 's')

    return s2


def from_sec(sec):
    return pd.to_datetime(sec, unit='s')


def get_darray_bounds(da: xr.DataArray):
    """get the bounds for the darray"""
    assert 'secs' in list(da.coords)
    assert 'lDp' in list(da.coords)

    t0, t1 = infer_interval_breaks(da['secs'])[[0, -1]]
    d0, d1 = infer_interval_breaks(da['lDp'])[[0, -1]]
    # t00 = (t0 - np.datetime64('1970')) / np.timedelta64(1, 's')
    # t11 = (t1 - np.datetime64('1970')) / np.timedelta64(1, 's')
    return d0, d1, t0, t1


class BananaPlotNodeCut(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "BananaPlotNodeCut"
    uiTemplate = [
        # {'name': 't1', 'type': 'float', 'value': 1e9},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        {'name': 'dock', 'type': 'str', 'value': nodeName},
        {
            'name' : 'log10',
            'type' : 'bool',
            'value': False,
            # 'limits': [0.001, 1],
            # 'dec'   : True,
            # 'step'  : .01
        },
        {
            'name' : 'auto range',
            'type' : 'bool',
            'value': False,
            # 'limits': [0.001, 1],
            # 'dec'   : True,
            # 'step'  : .01
        },

        {
            'name' : 'iso line',
            'type' : 'bool',
            'value': False,
            # 'limits': [0.001, 1],
            # 'dec'   : True,
            # 'step'  : .01
        }

    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            't1'    : dict(io='in'),
            't2'    : dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.dock = None
        # noinspection PyTypeChecker
        self.bp: BananaPlotCut = None

    # noinspection PyMethodOverriding
    def process(self, dataIn, t1, t2, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        # self.blockSignals(True)

        # print('entering bnnpltcut')

        dock_area = confg.dock_area

        # t1 = self.ctrls['t1']
        # t2 = self.ctrls['t2']
        duck_name = self.ctrls['dock'] = self.name()
        # self.ctrls['t3'] = np.random.randint(10)

        if duck_name not in dock_area.findAll()[1].keys():
            bp = BananaPlotCut(None)

            dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
            dock.addWidget(bp)
            dock_area.addDock(dock)

            confg.connectMasterXY(bp.plot_item, confg.par_tree)

            self.dock = dock
            self.bp = bp

        log10 = self.ctrls['log10']
        auto_range = self.ctrls['auto range']
        iso_line = self.ctrls['iso line']
        if self.bp is not None:
            self.bp.set_image_data_cut(dataIn, t1, t2, log10,
                                       auto_range=auto_range,
                                       iso=iso_line
                                       )
        # self.bp.set_region_ui(dataIn, t1, t2)

        if auto_range:
            self.bp.set_hist_levels(da=dataIn)
            self.bp.plot_item.enableAutoRange(axis='x', enable=True)

        self.blockSignals(False)

        return {}
