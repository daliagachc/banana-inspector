import numpy as np
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph import LinearRegionItem
from pyqtgraph.Qt import QtCore

from .. import confg
from .CtrlNodeTree import CtrlNodeTree

from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks


class BananaPlot(pg.GraphicsLayoutWidget):

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

        self.ci.addItem(hist)
        self.ci.addItem(plot_item)

        self.image_item = image_item
        self.plot_item = plot_item

        self.region: LinearRegionItem = None
        self.proxi = None

    def set_image_data(self, da):
        d2 = self.check_transpose(da)
        set_image_data(d2, self.image_item, True)

    def set_region_ui(self, da, t1=None, t2=None):
        vb = self.plot_item.vb
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot_item.addItem(vLine, ignoreBounds=True)
        self.plot_item.addItem(hLine, ignoreBounds=True)
        label = pg.LabelItem(justify='right')
        label.setText('')
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

    def set_image_data_cut(self, da, t1, t2):
        d_cut = da.loc[{'secs': slice(t1, t2)}]
        d2 = self.check_transpose(d_cut)
        set_image_data(d2, self.image_item, True)

    @staticmethod
    def check_transpose(da:xr.DataArray):
        order = ('secs', 'lDp')
        if da.dims != order:
            da1 = da.transpose(*order)
        else:
            da1 = da
        return da1


def set_image_data(da, img: pg.ImageItem, autoLevels):
    d0, d1, t00, t11 = get_darray_bounds(da)
    da = da.where(da > 1, 1)
    lda = np.log10(da)
    # lda = lda.where(lda>0,0)
    data = lda.values
    img.setImage(data, autoLevels=autoLevels)
    width = t11 - t00
    height = d1 - d0
    rect = QtCore.QRectF(t00, d0, width, height)
    img.setRect(rect)


def to_sec(date):
    s1 = date - np.datetime64(0, 'Y')
    s2 = s1 / np.timedelta64(1, 's')

    return s2


def from_sec(sec):
    return pd.to_datetime(sec, unit='s')


def get_darray_bounds(da: xr.DataArray):
    """get the bounds for the darray"""
    assert 'time' in list(da.coords)
    assert 'lDp' in list(da.coords)

    t0, t1 = infer_interval_breaks(da['time'])[[0, -1]]
    d0, d1 = infer_interval_breaks(da['lDp'])[[0, -1]]
    t00 = (t0 - np.datetime64('1970')) / np.timedelta64(1, 's')
    t11 = (t1 - np.datetime64('1970')) / np.timedelta64(1, 's')
    return d0, d1, t00, t11




class BananaPlotNodeRegion(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "BananaPlotNodeRegion"
    uiTemplate = [
        {'name': 't1', 'type': 'float', 'value': 1e9},
        {'name': 't2', 'type': 'float', 'value': 2e9},
        {'name': 't3', 'type': 'float', 'value': 2},
        {'name': 'dock', 'type': 'str', 'value': nodeName}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            't1': dict(io='out'),
            't2': dict(io='out'),
        }


        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.dock = None
        self.bp = None
        self.dataInSet = False
        self.dataIn = None


    def process(self, dataIn, display=True):
            # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

            # self.blockSignals(True)
            # print('reg')

            da = confg.dock_area

            self.ctrls.blockSignals(True)

            t1 = self.ctrls['t1']
            t2 = self.ctrls['t2']
            duck_name = self.ctrls['dock'] = self.name()
            self.ctrls['t3'] = np.random.randint(10)


            if duck_name not in da.findAll()[1].keys():
                bp = BananaPlot(None)

                dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
                dock.addWidget(bp)
                da.addDock(dock)

                #connect the cross hairs
                confg.connectMasterXY(bp.plot_item, confg.par_tree)

                self.dock = dock
                self.bp = bp

            if (dataIn is not None) and (self.dataInSet is False):
                self.dataInSet = True
                self.bp.set_image_data(dataIn)
                self.bp.set_region_ui(dataIn, t1, t2)

                t1, t2 = self.bp.region.getRegion()
                self.ctrls['t1'] = t1
                self.ctrls['t2'] = t2


                region = self.bp.region

                def reg_change():
                    print('change ggg ')
                    t1, t2 = region.getRegion()
                    # print(t1)
                    self.ctrls['t1'] = t1
                    self.ctrls['t2'] = t2

                region.sigRegionChangeFinished.connect(reg_change)
            else:
                # self.dataInSet = False
                pass

            # self.blockSignals(False)

            if id(dataIn) != id(self.dataIn):
                self.bp.set_image_data(dataIn)
                self.dataIn = dataIn

            self.ctrls.blockSignals(False)


            return {'t1': self.ctrls['t1'], 't2': self.ctrls['t2']}
