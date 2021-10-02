import numpy as np
import pandas as pd
import pyqtgraph as pg
import xarray as xr
from pyqtgraph import LinearRegionItem
from pyqtgraph.Qt import QtCore
import pyqtgraph.dockarea

from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks

from .CtrlNodeTree import CtrlNodeTree

from .. import confg


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

    def set_image_data(self, da):
        set_image_data(da, self.image_item, True)


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




class BananaPlotNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "BananaPlotNode"
    uiTemplate = [
        {'name': 'sigma', 'type': 'float', 'value': 1.0},
        {'name': 'strength', 'type': 'float', 'value': 1.0},
        {'name': 'dock', 'type': 'str', 'value': nodeName}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),  # each terminal needs at least a name and
            # 'dataOut': dict(io='out'),  # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNodeTree.__init__(self, name, terminals=terminals)
        self.dock = None
        self.bp = None

    def process(self, dataIn, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        # print('entering bnnpn')

        da = confg.dock_area

        # sigma = self.ctrls['sigma']
        # strength = self.ctrls['strength']
        duck_name = self.ctrls['dock'] = self.name()




        if duck_name not in da.findAll()[1].keys():
            bp = BananaPlot(None)

            dock = pyqtgraph.dockarea.Dock(duck_name,closable=True)
            dock.addWidget(bp)
            da.addDock(dock)

            #connect the chros hair attributes
            confg.connectMasterXY(bp.plot_item, confg.par_tree)

            self.dock = dock
            self.bp = bp



        self.bp.set_image_data(dataIn)

        return {}
