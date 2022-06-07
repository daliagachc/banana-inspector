# -*- coding: utf-8 -*-
"""
Demonstrates a way to put multiple axes around a single plot.

(This will eventually become a built-in feature of PlotItem)

"""
# import initExample ## Add path to library (just for examples; you do not need this)

from useful_scit.imps2.defs import *

from banana_inspector.util import bnn_array

p = '/Volumes/Transcend/diego_tr/flexpart-alto/flexpart_alto/data_big/v02_data_out/alto_cluster_timeseries_18.csv'

df = pd.read_csv(p)


df2 = df.set_index('sn_alto').T
df2.index.name = 'time'

df2.index = pd.to_datetime(df2.index)

ds2 = df2.to_xarray()

ds3 = ds2.bnn.set_sec()


import pyqtgraph as pg
import matplotlib.pyplot as plt


class MPlot:
    def __init__(self):

        cmap = plt.get_cmap('tab20')
        axisItems = {'bottom': pg.DateAxisItem(utcOffset=0)}
        pi:pg.PlotItem = pg.PlotItem(axisItems=axisItems)
        pw = pg.PlotWidget(plotItem=pi)

        #         pi = pw.plotItem

        self.pw: pg.PlotWidget = pw
        self.vbs = []
        self.pi: pg.PlotItem = pi
        self.colors = []
        self.labels = []
        self.yaxes = []
        self.cmap = cmap

    def add_first(self, label=None, color=None):
        if label is None:
            label = 'p1'
        if color is None:
            color = self._get_col(0)

        pi = self.pi
        pi.setLabels(left=label)
        ax = pi.getAxis('left')
        ax.setTextPen(color)
        ax.setWidth(60)

        self.vbs.append(pi.vb)
        self.colors.append(color)
        self.labels.append(label)
        self.yaxes.append(ax)

    def _get_col(self, ci):
        return pg.mkColor([int(255 * c) for c in self.cmap(ci)])

    #         self.add_second()

    def add_second(self, label=None, color=None):

        if label is None:
            label = 'p2'
        if color is None:
            color = self._get_col(1)

        vb2 = pg.ViewBox()
        self.pi.showAxis('right')
        self.pi.scene().addItem(vb2)
        yax = self.pi.getAxis('right')
        yax.linkToView(vb2)
        yax.setTextPen(color)
        vb2.setXLink(self.pi)
        yax.setLabel(label)
        self.vbs.append(vb2)
        self.colors.append(color)
        self.labels.append(label)
        self.yaxes.append(yax)
        yax.setWidth(60)
        ## Handle view resizing
        def updateViews():
            vb2.setGeometry(self.pi.vb.sceneBoundingRect())
            vb2.linkedViewChanged(self.pi.vb, vb2.XAxis)

        updateViews()
        self.pi.vb.sigResized.connect(updateViews)

    def add_extra(self, label=None, color=None):

        row_i = len(self.vbs)
        if label is None:
            label = f'p{row_i+1}'
        if color is None:
            color = self._get_col(row_i)

        vb3 = pg.ViewBox()
        ax3 = pg.AxisItem('right')
        ax3.setTextPen(color)
        p1 = self.pi
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

        def updateViews():
            vb3.setGeometry(self.pi.vb.sceneBoundingRect())
            vb3.linkedViewChanged(self.pi.vb, vb3.XAxis)

        updateViews()
        self.pi.vb.sigResized.connect(updateViews)
        return vb3

    def add_plot(self, label=None, color=None):
        if len(self.vbs) == 0:
            self.add_first(label=label,color=color)
        elif len(self.vbs) == 1:
            self.add_second(label=label,color=color)
        elif len(self.vbs) >= 2:
            self.add_extra(label=label,color=color)

    def plot_curve(self, i, data):
        vb = self.vbs[i]
        cc = self.colors[i]
        # currently if width > 1 it slow down the system
        pen = pg.mkPen(color=cc,width=1)
        x = data['secs'].values
        y = data.values
        vb.addItem(pg.PlotCurveItem(x=x,y=y, pen=pen))


pg.mkQApp()

pm = MPlot()
# pm.add_first()
# pm.add_second()
# pm.add_extra()
# pm.add_extra()
# pm.add_extra()

pw = pm.pw
pw.show()
pw.setWindowTitle('pyqtgraph example: MultiplePlotAxes')

# d1 = [10, 20, 40, 80, 60, 20]
# d2 = [10, 20, 40, 80, 40, 20]
# d3 = [3200, 1600, 800, 400, 200, 100]
# d4 = [3200, 1600, 800, 400, 200, 200]
# # d4 = []
# d5 = [3000, 1600, 800, 400, 200, 200]

# tt = [300,600,900,1200,1500,1800]

# d1 = xr.DataArray(d1,dims='secs',coords = {'secs':tt})
# d2 = xr.DataArray(d2,dims='secs',coords = {'secs':tt})
# d3 = xr.DataArray(d3,dims='secs',coords = {'secs':tt})
# d4 = xr.DataArray(d4,dims='secs',coords = {'secs':tt})
# d5 = xr.DataArray(d5,dims='secs',coords = {'secs':tt})


# dds = [d1, d2, d3, d4, d5]

# for i, d in enumerate(dds):
#     pm.plot_curve(i, d)

ds4 =ds3[{'secs':slice(0,200)}]
for i,l in enumerate(list(ds4.data_vars )[:18]):
    pm.add_plot(label=l)
    pm.plot_curve(i=i,data=ds4[l])