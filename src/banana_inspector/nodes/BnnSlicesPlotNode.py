import time

import pyqtgraph as pg
import xarray as xr
from pyqtgraph.Qt import QtGui

from .CtrlNodeTree import CtrlNodeTree
import pyqtgraph.dockarea

from .. import confg


class BnnSlicesPlot:
    def __init__(self, name=None):
        grid_layout, wl = self.set_up_widget()
        self.grid_layout = grid_layout
        self.widget_layout = wl

        self.rows = None

        self.Dps = None

    def set_up_plots(self, da: xr.DataArray):
        series = da['lDp'].to_series()
        s2 = series.sort_values().reset_index(drop=True).reset_index().set_index('lDp')
        # s3 = s2.to_dataframe()
        # return s2
        dic = s2.transpose().to_dict()

        l_dic = len(dic)

        for ii, (ldp, r) in enumerate(dic.items()):
            index_ = r['index']
            dic[ldp]['j'] = l_dic - index_

            pw: pg.GraphicsLayout = pg.GraphicsLayoutWidget()
            dic[ldp]['pw'] = pw

            xax = pg.DateAxisItem(utcOffset=0)
            axisItems = {'bottom': xax}
            pi = pg.PlotItem(axisItems=axisItems)

            # pi = pg.PlotItem()
            dic[ldp]['pi'] = pi

            pw.addItem(pi, row=1, col=1)

            j_ = r['j']
            self.widget_layout.addWidget(pw, row=j_, col=1)
            pi.getAxis('left').setWidth(80)
            pi.setLimits(yMin=0)
            if ii == 0:
                pi0 = pi
            if ii != 0:
                pi.setXLink(pi0)

            ci = pg.PlotCurveItem(pen=(0,0,255))

            dic[ldp]['ci'] = ci

            pi.addItem(ci)

        self.Dps = dic

        self.plot_curves((255,0,0), da)

    def plot_curves(self, col, da):
        for ldp, r in self.Dps.items():
            ci = r['ci']

            # pi:pg.PlotItem

            # if 'ci' in r.keys():
            #     ci = r['ci']
            #     pi.removeItem(ci
            # dic[ldp]['ci'] = ci
            # print(ldp)
            # print(r['j'])
            di = da.loc[{'lDp': ldp}].reset_coords(drop=True).to_series().reset_index()
            ci.setData(di['secs'].values, di['dndlDp'].values)

    @staticmethod
    def set_up_widget():

        gridLayout = QtGui.QGridLayout()
        gridLayout.setObjectName(u"gridLayout")
        scrollArea = QtGui.QScrollArea()
        scrollArea.setObjectName(u"scrollArea")
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtGui.QWidget()
        scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        gridLayout_3 = QtGui.QGridLayout(scrollAreaWidgetContents)
        gridLayout_3.setObjectName(u"gridLayout_3")
        gridLayout_2 = QtGui.QGridLayout()
        gridLayout_2.setObjectName(u"gridLayout_2")
        scrollArea.setWidget(scrollAreaWidgetContents)
        gridLayout = pg.LayoutWidget()
        gridLayout.addWidget(scrollArea, 0, 0, 1, 1)
        gridLayout_3.addLayout(gridLayout_2, 0, 0, 1, 1)
        wl = pg.LayoutWidget()
        gridLayout_2.addWidget(wl)
        scrollAreaWidgetContents.setMinimumHeight(5000)
        return gridLayout, wl


class BnnSlicesPlotNode(CtrlNodeTree):
    """Return the input data passed through an unsharp mask."""
    nodeName = "BnnSlicesPlotNode"
    uiTemplate = [
        # {'name': 't1', 'type': 'float', 'value': 1e9},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        # {'name': 'dock', 'type': 'str', 'value': 'BnnPlotCut'}
        {'name': 'dock', 'type': 'str', 'value': 'BnnSlicesDock'}
    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn': dict(io='in'),
            # 'dataOut': dict(io='out'),
            # 't1': dict(io='in'),
            # 't2': dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.dock = None
        self.bnn_slices_plot = None
        self.dataInSet = False
        self.time_last_set = 0

    # noinspection PyMethodOverriding
    def process(self, dataIn:xr.DataArray, display=True):
        print('entering process')
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        da = confg.dock_area

        # t1 = self.ctrls['t1']
        # t2 = self.ctrls['t2']
        duck_name = self.ctrls['dock']


        if duck_name not in da.findAll()[1].keys():
            bnn_slices_plot = BnnSlicesPlot()

            dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
            dock.addWidget(bnn_slices_plot.grid_layout)
            da.addDock(dock)

            self.bnn_slices_plot = bnn_slices_plot



            # bnn_slices_plot.plot_curves((0,255,0),dataIn)

            self.dock = dock



            # self.bp.set_image_data(dataIn)
            # self.bp.set_region_ui(dataIn, t1, t2)
            #
            # t1, t2 = self.bp.region.getRegion()
            # self.ctrls['t1'] = t1
            # self.ctrls['t2'] = t2
            #
            #
            # region = self.bp.region
            #
            # def reg_change():
            #     t1, t2 = region.getRegion()
            #     print(t1)
                # self.ctrls['t1'] = t1
                # self.ctrls['t2'] = t2
            #
            # region.sigRegionChangeFinished.connect(reg_change)
        if self.dataInSet is False:
            if dataIn is not None:
                print('none none')
                self.dataInSet = True
                self.bnn_slices_plot.set_up_plots(dataIn)
                # self.bnn_slices_plot =bnn_slices_plot

        if (dataIn is not None):
            # if (time.time() - self.time_last_set > 1 ):
            if True:
                # self.blockSignals(True)

                self.time_last_set = time.time()
                print('setting data')
                self.bnn_slices_plot.plot_curves((0,255,0),dataIn)

                self.blockSignals(False)

        return {}
