# import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg
import pyqtgraph.dockarea

from .CtrlNodeTree import CtrlNodeTree
from .. import confg


# import xarray as xr
# from pyqtgraph import LinearRegionItem
# from pyqtgraph.Qt import QtCore
# noinspection PyProtectedMember
# from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks

class CurvePlot(pg.GraphicsLayoutWidget):
    def __init__(self, parent, color1=None, color2 = None, **kargs):
        super().__init__(parent=parent, **kargs)

        cmap = plt.get_cmap('tab20')
        axisItems = {'bottom': pg.DateAxisItem(utcOffset=0)}
        pi: pg.PlotItem = pg.PlotItem(axisItems=axisItems)

        # pw = pg.PlotWidget(plotItem=pi)

        #         pi = pw.plotItem

        self.ci.addItem(pi)

        # self.pw: pg.PlotWidget = pw
        self.vbs = []
        self.plot_item: pg.PlotItem = pi
        self.colors = []
        self.labels = []
        self.yaxes = []
        self.p_curve_items = []
        self.cmap = cmap
        self.proxy = None

        pi.setXLink(confg.dummy_plot_item_1)
        self.add_plot(color=color1)
        self.add_plot(color=color2)

    def add_first(self, label=None, color=None):
        if label is None:
            label = 'p1'
        if color is None:
            color = self._get_col(0)

        pi = self.plot_item
        pi.setLabels(left=label)
        ax = pi.getAxis('left')
        ax.setTextPen(color)
        ax.setWidth(60)

        pci = pg.PlotCurveItem()
        self.plot_item.addItem(pci)

        self.vbs.append(pi.vb)
        self.colors.append(color)
        self.labels.append(label)
        self.yaxes.append(ax)
        self.p_curve_items.append(pci)

    def _get_col(self, ci):
        return pg.mkColor([int(255 * c) for c in self.cmap(ci)])

    #         self.add_second()

    def add_second(self, label=None, color=None):

        if label is None:
            label = 'p2'
        if color is None:
            color = self._get_col(1)

        vb2 = pg.ViewBox()
        self.plot_item.showAxis('right')
        self.plot_item.scene().addItem(vb2)
        yax = self.plot_item.getAxis('right')
        yax.linkToView(vb2)
        yax.setTextPen(color)
        vb2.setXLink(self.plot_item)
        yax.setLabel(label)
        self.vbs.append(vb2)
        self.colors.append(color)
        self.labels.append(label)
        self.yaxes.append(yax)
        yax.setWidth(60)

        ## Handle view resizing
        def updateViews():
            vb2.setGeometry(self.plot_item.vb.sceneBoundingRect())
            vb2.linkedViewChanged(self.plot_item.vb, vb2.XAxis)

        updateViews()
        self.plot_item.vb.sigResized.connect(updateViews)

        pci = pg.PlotCurveItem()
        vb2.addItem(pci)
        self.p_curve_items.append(pci)

    def add_extra(self, label=None, color=None):

        row_i = len(self.vbs)
        if label is None:
            label = f'p{row_i + 1}'
        if color is None:
            color = self._get_col(row_i)

        vb3 = pg.ViewBox()
        ax3 = pg.AxisItem('right')
        ax3.setTextPen(color)
        p1 = self.plot_item
        p1.layout.addItem(ax3, 2, row_i + 1)
        p1.scene().addItem(vb3)
        ax3.linkToView(vb3)
        vb3.setXLink(p1)
        ax3.setZValue(-10000)
        ax3.setLabel(label)
        self.vbs.append(vb3)
        self.colors.append(color)
        self.labels.append(label)
        self.yaxes.append(ax3)
        ax3.setWidth(60)

        pci = pg.PlotCurveItem()
        self.p_curve_items.append(pci)
        # self.plot_item.addItem(pci)
        vb3.addItem(pci)

        def updateViews():
            vb3.setGeometry(self.plot_item.vb.sceneBoundingRect())
            vb3.linkedViewChanged(self.plot_item.vb, vb3.XAxis)

        updateViews()
        self.plot_item.vb.sigResized.connect(updateViews)
        return vb3

    def add_plot(self, label=None, color=None):
        if len(self.vbs) == 0:
            self.add_first(label=label, color=color)
        elif len(self.vbs) == 1:
            self.add_second(label=label, color=color)
        elif len(self.vbs) >= 2:
            self.add_extra(label=label, color=color)

    def plot_curve(self, i, data, color):
        # vb = self.vbs[i]
        if color is None:
            cc = self.colors[i]
        else:
            cc = color
            self.colors[i] = color
        # currently if width > 1 it slow down the system
        pen = pg.mkPen(color=cc, width=1)
        x = data['secs'].values
        y = data.values

        pci: pg.PlotCurveItem = self.p_curve_items[i]
        pci.setData(x=x, y=y, pen=pen)

        # vb.addItem(pg.PlotCurveItem(x=x,y=y, pen=pen))

    def set_curve(self, i, dataIn, t1, t2,
                  auto_range,
                  color = None
                  ):

        if color is None:
            cc = self.colors[i]
        else:
            cc = color
            self.colors[i] = color


        if dataIn is None:
            return



        dataIn_ = dataIn.loc[{'secs': slice(t1, t2)}]

        self.plot_curve(i, dataIn_,color = cc )
        if auto_range:
            self.plot_item.enableAutoRange(axis='x', enable=True)


class CurvePlotNode(CtrlNodeTree):
    """plots a cruve plot. multiline """
    nodeName = "CurvePlotNode"
    uiTemplate = [
        # {'name': 't1', 'type': 'float', 'value': 1e9},
        # {'name': 't2', 'type': 'float', 'value': 2e9},
        # {'name': 't3', 'type': 'float', 'value': 2},
        {'name': 'dock', 'type': 'str', 'value': nodeName},
        {'name': 'title', 'type': 'str', 'value': ''},
        {'name': 'ylab1', 'type': 'str', 'value': 'p1'},
        {'name': 'color1', 'type': 'color', 'value': None},
        {'name': 'ylab2', 'type': 'str', 'value': 'p2'},
        {'name': 'color2', 'type': 'color', 'value': None},
        # {
        #     'name' : 'log10',
        #     'type' : 'bool',
        #     'value': False,
        #     # 'limits': [0.001, 1],
        #     # 'dec'   : True,
        #     # 'step'  : .01
        # },
        {
            'name' : 'auto range',
            'type' : 'bool',
            'value': False,
            # 'limits': [0.001, 1],
            # 'dec'   : True,
            # 'step'  : .01
        },

        # {
        #     'name' : 'iso line',
        #     'type' : 'bool',
        #     'value': False,
        #     # 'limits': [0.001, 1],
        #     # 'dec'   : True,
        #     # 'step'  : .01
        # }

    ]

    def __init__(self, name):
        ## Define the input / output terminals available on this node
        terminals = {
            'dataIn_1': dict(io='in'),
            'dataIn_2': dict(io='in'),
            't1'      : dict(io='in'),
            't2'      : dict(io='in'),
        }

        CtrlNodeTree.__init__(self, name, terminals=terminals)

        self.dock = None
        # noinspection PyTypeChecker
        self.curve_plot: CurvePlot = None

    # noinspection PyMethodOverriding
    def process(self,
                dataIn_1=None, dataIn_2=None,
                t1=None, t2=None, display=True):
        # CtrlNode has created self.ctrls, which is a dict containing {ctrlName: widget}

        # self.blockSignals(True)

        # print('entering bnnpltcut')

        dock_area = confg.dock_area

        # t1 = self.ctrls['t1']
        # t2 = self.ctrls['t2']
        duck_name = self.ctrls['dock'] = self.name()
        # self.ctrls['t3'] = np.random.randint(10)

        color1 = self.ctrls['color1']
        color2 = self.ctrls['color2']

        if duck_name not in dock_area.findAll()[1].keys():
            curve_plot = CurvePlot(None, color1=color1,color2=color2)
            if color1 is None:
                color1 = curve_plot.colors[0]
                self.ctrls['color1'] = color1
            if color2 is None:
                color2 = curve_plot.colors[1]
                self.ctrls['color2'] = color2



            dock = pyqtgraph.dockarea.Dock(duck_name, closable=True)
            dock.addWidget(curve_plot)
            dock_area.addDock(dock)

            confg.connectMasterX(curve_plot.plot_item, confg.par_tree)

            self.dock = dock
            self.curve_plot: CurvePlot = curve_plot

        # log10 = self.ctrls['log10']
        auto_range = self.ctrls['auto range']
        # iso_line = self.ctrls['iso line']
        if self.curve_plot is not None:
            cv = self.curve_plot
            cv.set_curve(0, dataIn_1, t1, t2,
                         # log10,
                         auto_range=auto_range,
                         # iso=iso_line,
                         color = color1

                         )
            cv.set_curve(1, dataIn_2, t1, t2,
                         # log10,
                         auto_range=auto_range,
                         # iso=iso_line
                         color = color2
                         )
            # self.curve_plot.set_region_ui(dataIn, t1, t2)
            ylab1 = self.ctrls['ylab1']
            ylab2 = self.ctrls['ylab2']

            ya1 = cv.yaxes[0]
            ya2 = cv.yaxes[1]

            ya1.setTextPen(color1)
            ya2.setTextPen(color2)

            ya1.setLabel(ylab1)
            ya2.setLabel(ylab2)

        if auto_range:
            # self.curve_plot.set_hist_levels(da=dataIn)
            self.curve_plot.plot_item.enableAutoRange(axis='x', enable=True)

        self.blockSignals(False)

        return {}
