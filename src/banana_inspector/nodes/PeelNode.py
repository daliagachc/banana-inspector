import os

import numpy as np
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.dockarea
import xarray as xr
from pyqtgraph import LinearRegionItem
from pyqtgraph.Qt import QtCore
from pyqtgraph.configfile import writeConfigFile, readConfigFile
from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks

from . import logBnn
from .CtrlNodeTree import CtrlNodeTree
from .. import confg


class PeelPlot(pg.GraphicsLayoutWidget):

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
        self.ctrls = None
        self.roi = None

        def updateIsocurve():
            iso.setLevel(isoLine.value())

        isoLine.sigDragged.connect(updateIsocurve)

        self.ci.addItem(hist)
        self.ci.addItem(plot_item)

        self.image_item = image_item
        self.plot_item = plot_item

        # noinspection PyTypeChecker
        self.region: LinearRegionItem = None
        self.proxi = None
        self.hist = hist
        self.image_item = image_item
        self.iso = iso
        self.isoLine = isoLine
        self.roi = None

    def create_roi(self):
        logBnn.ger.debug('creating roi')
        if self.roi is not None:
            self.plot_item.removeItem(self.roi)
        plot_item = self.plot_item
        (x1, x2), (y1, y2) = plot_item.viewRange()

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        xd = x2 - x1
        yd = y2 - y1

        roi = pg.PolyLineROI([
            [x - (1 / 2) * xd, y1],
            [x + (1 / 2) * xd, y1],
            [x, y + yd / 2]],
            closed=True)

        plot_item.addItem(roi)

        self.roi = roi

    def remove_peel(self):
        r = self.roi
        pi = self.plot_item
        pi.removeItem(r)

    def save_peel(self):
        # xy = self.bp.get_roi_pol_coords()
        id1 = self.get_roi_id()
        self.ctrls['id'] = id1

        path = self.ctrls['project dir']

        if path is None:
            path = '.'

        id2 = os.path.join(path, id1 + '.txt')

        out_dic = {}

        s = self.ctrls.saveState()

        if self.roi is None:
            raise Exception('roi does not exist')
        else:
            r = self.roi.saveState()

        out_dic['par'] = s
        out_dic['roi'] = r

        if os.path.isfile(id2) is False:
            writeConfigFile(out_dic, id2)
        else:
            # raise Exception('file exists')
            # logBnn.ger.info('node exists!')
            '''save anyways'''
            writeConfigFile(out_dic, id2)

    def get_roi_pol_coords(self):
        """gets the ROI list of coords in the axis mapping"""
        pts = self.roi.getState()['points']
        pts = [self.roi.mapToParent(p) for p in pts]
        pts1 = [[p.x(), p.y()] for p in pts]
        pts2 = np.array(pts1)

        return pts2

    def get_roi_id(self):
        xy = self.get_roi_pol_coords()

        # self.bp.ctrls['id'] = id1

        path = self.ctrls['project dir']

        df = pd.DataFrame(xy, columns=['x', 'y'])

        t = df.sort_values('y')[:2]['x'].mean()

        tt = pd.to_datetime(t * 1e9)

        tid = tt.strftime('%Y-%m-%d_%H')
        return tid

    def set_image_data(self, da, log10):
        d2 = self.check_transpose(da)
        self._set_image_data(d2, True, log10)

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

    def set_image_data_cut(self, da, t1, t2, log10, auto_range):
        d_cut = da.loc[{'secs': slice(t1, t2)}]
        d2 = self.check_transpose(d_cut)
        self._set_image_data(d2, auto_range, log10)

    @staticmethod
    def check_transpose(da: xr.DataArray):
        order = ('secs', 'lDp')
        if da.dims != order:
            da1 = da.transpose(*order)
        else:
            da1 = da
        return da1

    def _set_image_data(self, da, autoLevels, log10):
        img: pg.ImageItem = self.image_item
        d0, d1, t00, t11 = get_darray_bounds(da)
        if log10:
            da = da.where(da > 1, 1)
            lda = np.log10(da)
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


class PeelNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "PeelNode"
    uiTemplate = [
        {
            'name' : 'id',
            'type' : 'str',
            'value': '',
            # 'limits': [0.0001,2],
            # 'dec'   : True,
            # 'step'  : .1
        },
        {
            'name'  : 'qQ',
            'type'  : 'float',
            'value' : .5,
            'limits': [0.001, 1],
            'dec'   : True,
            'step'  : .01
        },
        {
            'name'  : 'qR',
            'type'  : 'float',
            'value' : .5,
            'limits': [0.001, 1],
            'dec'   : True,
            'step'  : .01
        },
        {
            'name' : 'd1',
            'type' : 'float',
            'value': -9,
            # 'limits': [0.00, 1],
            'dec'  : True,
            'step' : .1
        },
        {
            'name' : 'd2',
            'type' : 'float',
            'value': -8,
            # 'limits': [0.00, 1],
            'dec'  : True,
            'step' : .1
        },
        {
            'name' : 'd3',
            'type' : 'float',
            'value': -6,
            # 'limits': [0.00, 1],
            'dec'  : True,
            'step' : .1
        },
        {
            'name' : 'text',
            'type' : 'text',
            'value': '',
            # 'limits': [0.001, 1],
            # 'dec'   : True,
            # 'step'  : .01
        },
        {
            'name': 'fit peel',
            'type': 'action',
            # 'value': 0.00,
            # 'readonly': True
        },
        {
            'name': 'save peel',
            'type': 'action',
            # 'value': 0.00,
            # 'readonly': True
        },
        {
            'name': 'create peel',
            'type': 'action',
            # 'value': 0.00,
            # 'readonly': True
        },

        {
            'name': 'open peel',
            'type': 'action',
            # 'value': 0.00,
            # 'readonly': True
        },
        {
            'name': 'remove peel',
            'type': 'action',
            # 'value': 0.00,
            # 'readonly': True
        },

        {
            'name'    : 'project dir',
            'type'    : 'file',
            'fileMode': 'Directory',
            # 'default' : '/tmp/',
        },

        {
            'name'      : 'to open file',
            'type'      : 'file',
            'fileMode'  : 'AnyFile',
            'acceptMode': 'AcceptOpen',
            # 'default'   : '/tmp/ff.cf',
        },

        {'name' : 'dock',
         'type' : 'str',
         'value': nodeName}
        ,
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
        }
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn'    : dict(io='in'),
            't1'        : dict(io='in'),
            't2'        : dict(io='in'),
            'ridge_node': dict(io='in'),
            'qnorm_node': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.dock = None
        # noinspection PyTypeChecker
        self.bp: PeelPlot = None

        self.ridge_node = None
        self.qnorm_node = None
        self.scatter = None
        self.scatter1 = None
        self.df_fit: pd.DataFrame = None

    def fit_peel(self):
        try:
            self.df_fit = None
            if self.scatter is not None:
                self.bp.plot_item.removeItem(self.scatter)
                self.bp.plot_item.removeItem(self.scatter1)
            import banana_inspector.util.get_gr as gr
            qQ = self.ctrls['qQ']
            qR = self.ctrls['qR']
            d1 = self.ctrls['d1']
            d2 = self.ctrls['d2']
            d3 = self.ctrls['d3']
            qnorm_node = self.qnorm_node
            ridge_node = self.ridge_node

            roi = self.bp.get_roi_pol_coords()
            roi = np.array([*roi, roi[0]])

            df = gr.get_gr(qnorm_node,
                           ridge_node,
                           qq=qQ,
                           qq2=qR,
                           d1=d1,
                           d2=d2,
                           d3=d3,
                           roi=roi)

            y = 10 ** df['y'].values
            yf = 10 ** df['y_fit'].values
            x = df['x'].values
            di = self.bp.plot_item.scatterPlot()
            di2 = self.bp.plot_item.scatterPlot()
            di.setData(x=x, y=y,
                       pen=(0, 0, 0),
                       symbolBrush=(0, 255, 0), symbolPen='w', symbol='x',
                       symbolSize=14, name="y")

            di2.setData(x=x, y=yf,
                        pen=(0, 0, 0),
                        symbolBrush=(0, 255, 0), symbolPen='w', symbol='o',
                        symbolSize=14, name="y")

            self.scatter = di
            self.scatter1 = di2
            self.df_fit = df
        except:
            pass

        pass

    def save_peel(self):
        self.bp.save_peel()
        if self.df_fit is not None:
            path = self.ctrls['project dir']
            if path is None:
                path = './'
            id = self.ctrls['id'] + '.csv'
            id2 = os.path.join(path, id)
            self.df_fit.to_csv(id2)

    def open_peel(self):
        p = self.ctrls['to open file']
        prd = self.ctrls['project dir']
        readConfigFile(p)
        cf = readConfigFile(p)
        cf.keys()
        cfr = cf['roi']
        cfp = cf['par']
        self.ctrls.restoreState(cfp)
        roi = self.bp.roi
        if roi is not None:
            self.bp.remove_peel()
        self.bp.create_roi()
        roi = self.bp.roi
        roi.setPos(cfr['pos'])
        roi.setPoints(cfr['points'])
        self.ctrls['to open file'] = p
        self.ctrls['project dir'] = prd

    # noinspection PyMethodOverriding
    def process(self, dataIn, t1, t2, qnorm_node, ridge_node, display=True):

        self.ridge_node = ridge_node
        self.qnorm_node = qnorm_node

        if self.bp is not None:
            if self.bp.roi is not None:
                try:
                    self.fit_peel()
                except:
                    logBnn.ger.info('cant fit ')
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        # self.blockSignals(True)

        # print('entering bnnpltcut')

        dock_area = confg.dock_area

        # t1 = self.ctrls['t1']
        # t2 = self.ctrls['t2']
        duck_name = self.ctrls['dock'] = self.name()
        # self.ctrls['t3'] = np.random.randint(10)

        if duck_name not in dock_area.findAll()[1].keys():
            bp = PeelPlot(None)

            dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
            dock.addWidget(bp)
            dock_area.addDock(dock)

            confg.connectMasterXY(bp.plot_item, confg.par_tree)

            self.dock = dock
            self.bp: PeelPlot = bp
            self.bp.ctrls = self.ctrls

            param = self.ctrls.param('create peel')
            param.sigActivated.connect(self.bp.create_roi)

            param = self.ctrls.param('remove peel')
            param.sigActivated.connect(self.bp.remove_peel)

            param = self.ctrls.param('save peel')
            param.sigActivated.connect(self.save_peel)

            param = self.ctrls.param('fit peel')
            param.sigActivated.connect(self.fit_peel)

            param = self.ctrls.param('open peel')
            param.sigActivated.connect(self.open_peel)

        log10 = self.ctrls['log10']
        auto_range = self.ctrls['auto range']
        if self.bp is not None:
            self.bp.set_image_data_cut(dataIn, t1, t2, log10, auto_range=auto_range)
        # self.bp.set_region_ui(dataIn, t1, t2)

        if auto_range:
            self.bp.set_hist_levels(da=dataIn)
            self.bp.plot_item.enableAutoRange(axis='x', enable=True)

        self.blockSignals(False)

        return {}
