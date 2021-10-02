import numpy as np
import pandas as pd
import pyqtgraph as pg
import xarray as xr
from pyqtgraph import LinearRegionItem
from pyqtgraph.Qt import QtCore
import pyqtgraph.dockarea

from pyqtgraph.graphicsItems.NonUniformImage import NonUniformImage

from CtrlNodeTree import CtrlNodeTree

from .. import confg


class IrregularBnnPlt(pg.GraphicsLayoutWidget):

    def __init__(self, parent, **kargs):
        super().__init__(parent=parent, **kargs)

        # self.time_axis = pg.DateAxisItem( utcOffset=0 )

        axisItems = {'bottom': pg.DateAxisItem(utcOffset=0)}
        plot_item: pg.PlotItem = pg.PlotItem(axisItems=axisItems)

        plot_item.setTitle("log( dN /dlog(Dp) )")
        # plot_item.setAxisItems()
        plot_item.setLogMode(x=None, y=True)
        # pg.ImageItem
        image_item = NonUniformImage()
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


def _is_monotonic(coord, axis=0):
    """
    >>> _is_monotonic(np.array([0, 1, 2]))
    True
    >>> _is_monotonic(np.array([2, 1, 0]))
    True
    >>> _is_monotonic(np.array([0, 2, 1]))
    False
    """
    if coord.shape[axis] < 3:
        return True
    else:
        n = coord.shape[axis]
        delta_pos = coord.take(np.arange(1, n), axis=axis) >= coord.take(
            np.arange(0, n - 1), axis=axis)
        delta_neg = coord.take(np.arange(1, n), axis=axis) <= coord.take(
            np.arange(0, n - 1), axis=axis)
        return np.all(delta_pos) or np.all(delta_neg)


def infer_interval_breaks(coord, axis=0, check_monotonic=False):
    """
    >>> infer_interval_breaks(np.arange(5))
    array([-0.5,  0.5,  1.5,  2.5,  3.5,  4.5])
    >>> infer_interval_breaks([[0, 1], [3, 4]], axis=1)
    array([[-0.5,  0.5,  1.5],
           [ 2.5,  3.5,  4.5]])
    """
    coord = np.asarray(coord)

    if check_monotonic and not _is_monotonic(coord, axis=axis):
        raise ValueError("The input coordinate is not sorted in increasing "
                         "order along axis %d. This can lead to unexpected "
                         "results. Consider calling the `sortby` method on "
                         "the input DataArray. To plot data with categorical "
                         "axes, consider using the `heatmap` function from "
                         "the `seaborn` statistical plotting library." % axis)

    deltas = 0.5 * np.diff(coord, axis=axis)
    if deltas.size == 0:
        deltas = np.array(0.0)
    first = np.take(coord, [0], axis=axis) - np.take(deltas, [0],
                                                     axis=axis)
    last = np.take(coord, [-1], axis=axis) + np.take(deltas, [-1],
                                                     axis=axis)
    trim_last = tuple(
        slice(None, -1) if n == axis else slice(None) for n in
        range(coord.ndim))
    return np.concatenate([first, coord[trim_last] + deltas, last],
                          axis=axis)


class IrregularBnnPltNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "IrregularBnnPltNode"
    uiTemplate = [
        {'name': 'sigma', 'type': 'float', 'value': 1.0},
        {'name': 'strength', 'type': 'float', 'value': 1.0},
        {'name': 'dock', 'type': 'str', 'value': 'BPlotDuck'}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),  # each terminal needs at least a name and
            # 'dataOut': dict(io='out'),  # to specify whether it is input or output
        }  # other more advanced options are available
        # as well..

        CtrlNodeTree.__init__(self, name, terminals=terminals)

    def process(self, dataIn, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        da = confg.dock_area

        sigma = self.ctrls['sigma']
        strength = self.ctrls['strength']
        duck_name = self.ctrls['dock']

        self.dock = None
        self.bp = None


        if duck_name not in da.findAll()[1].keys():
            bp = IrregularBnnPlt(None)

            dock = pyqtgraph.dockarea.Dock(duck_name,closable=True)
            dock.addWidget(bp)
            da.addDock(dock)

            self.dock = dock
            self.bp = bp


        self.bp.set_image_data(dataIn)

        return {}
