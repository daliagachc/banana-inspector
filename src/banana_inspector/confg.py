import pandas as pd
import pyqtgraph as pg
import pyqtgraph.dockarea
import pyqtgraph.flowchart
import pyqtgraph.parametertree
from pyqtgraph.Qt import QtWidgets

from .util.true_eq import eq

pyqtgraph.functions.eq = eq
'''lets fix pyqtgraph equivalence function so 
that it also takes into account xarrays'''

# this is the template for the monkey-tools
_ui = [
    {
        'name'    : 'mX',
        'type'    : 'float',
        'value'   : 0.,
        'readonly': True
    },
    {
        'name'    : 'secs',
        'type'    : 'int',
        'value'   : 0,
        'readonly': True
    },
    {
        'name'    : 'date',
        'type'    : 'str',
        'value'   : '',
        'readonly': True
    },
    {
        'name'    : 'mY',
        'type'    : 'float',
        'value'   : 0.00,
        'readonly': True
    },

    {
        'name'    : 'Dp',
        'type'    : 'float',
        'value'   : 0.00,
        'readonly': True
    },
    {
        'name': 'save project',
        'type': 'action',
        # 'value': 0.00,
        # 'readonly': True
    },

    {
        'name': 'open project',
        'type': 'action',
        # 'value': 0.00,
        # 'readonly': True
    },

    {'name'    : 'project dir',
     'type'    : 'file',
     'fileMode': 'Directory',
     # 'default' : '/tmp/',
     },

    {'name'      : 'file proj',
     'type'      : 'file',
     'fileMode'  : 'AnyFile',
     'acceptMode': 'AcceptSave',
     # 'default'   : '/tmp/ff.cf',
     }
]

par_tree = pyqtgraph.parametertree.Parameter.create(
    name='masterXY', type='group', children=_ui)

dock_area: pyqtgraph.dockarea.DockArea = None
'''this is the global dock area'''

main_window: QtWidgets.QMainWindow = None
'''this is the main bnn-app'''

main_fchart: pg.flowchart.Flowchart = None
'''this is the main flow chart'''

main_app = None
'''this is the basice app and is stored here'''

dock_mnk_tool:pyqtgraph.dockarea.DockArea = None
'''as in monkey_tool this is set up by '''

dummy_plot_item_1 = None
'''dummy plot to hold references to x and y axis'''


class connectMasterXY:
    def __init__(self, plot_item: pg.PlotItem, par_tree: pg.parametertree.ParameterTree):
        # cross hair
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        plot_item.addItem(vLine, ignoreBounds=True)
        plot_item.addItem(hLine, ignoreBounds=True)
        vb = plot_item.vb

        def mouseMoved(evt):
            #             p.blockSignals(True)
            #             self.proxy.blockSignals(True)

            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if plot_item.sceneBoundingRect().contains(pos):
                mousePoint = vb.mapSceneToView(pos)
                # index = int(mousePoint.x())
                vLine.setPos(mousePoint.x())
                hLine.setPos(mousePoint.y())
                par_tree['mX'] = mousePoint.x()
                par_tree['mY'] = mousePoint.y()

                par_tree['Dp'] = 10 ** par_tree['mY'] * 1e9
                par_tree['secs'] = int(par_tree['mX'])
                ts = pd.to_datetime(par_tree['mX'] * 1e9)
                par_tree['date'] = ts.strftime('%Y-%m-%d %X')

        #             self.proxy.blockSignals(False)
        #             p.blockSignals(False)
        #             p.sigTreeStateChanged.emit(1,1)

        self.proxy = pg.SignalProxy(plot_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

        self.vl = vLine
        self.hl = hLine

        def dd():
            try:

                self.vl.setPos(par_tree['mX'])
                self.hl.setPos(par_tree['mY'])


            except RuntimeError:
                print('ive been deleted?')

        par_tree.sigTreeStateChanged.connect(dd)


class connectMasterX:
    def __init__(self, plot_item: pg.PlotItem, par_tree: pg.parametertree.ParameterTree):
        # cross hair
        vLine = pg.InfiniteLine(angle=90, movable=False)
        # hLine = pg.InfiniteLine(angle=0, movable=False)
        plot_item.addItem(vLine, ignoreBounds=True)
        # plot_item.addItem(hLine, ignoreBounds=True)
        vb = plot_item.vb

        def mouseMoved(evt):
            #             p.blockSignals(True)
            #             self.proxy.blockSignals(True)

            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if plot_item.sceneBoundingRect().contains(pos):
                mousePoint = vb.mapSceneToView(pos)
                # index = int(mousePoint.x())
                vLine.setPos(mousePoint.x())
                # hLine.setPos(mousePoint.y())
                par_tree['mX'] = mousePoint.x()
                # par_tree['mY'] = mousePoint.y()

                # par_tree['Dp'] = 10 ** par_tree['mY'] * 1e9
                par_tree['secs'] = int(par_tree['mX'])
                ts = pd.to_datetime(par_tree['mX'] * 1e9)
                par_tree['date'] = ts.strftime('%Y-%m-%d %X')

        #             self.proxy.blockSignals(False)
        #             p.blockSignals(False)
        #             p.sigTreeStateChanged.emit(1,1)

        self.proxy = pg.SignalProxy(plot_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

        self.vl = vLine
        # self.hl = hLine

        def dd():
            try:

                self.vl.setPos(par_tree['mX'])
                # self.hl.setPos(par_tree['mY'])


            except RuntimeError:
                print('ive been deleted?')

        par_tree.sigTreeStateChanged.connect(dd)