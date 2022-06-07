'''
this is the basic app where all other layouts
should be built upon
'''

import os
import pyqtgraph as pg
# import pyqtgraph.console
import pyqtgraph.dockarea
import pyqtgraph.flowchart
from pyqtgraph.Qt import QtWidgets,QtGui

from ..util import console

# from .. import util.console

from ..util import log_bnn as lg
from .. import confg

from .. import resources
icon_path = resources.__path__[0]

app = pg.mkQApp()

path = os.path.join(icon_path, 'icon.png')
app.setWindowIcon(QtGui.QIcon(path))

confg.main_window = mw = QtWidgets.QMainWindow()
mw.resize(1000, 800)

confg.dock_area = da = pg.dockarea.DockArea()
confg.dock_mnk_tool = dck_mt = pg.dockarea.Dock('mnk-tool')
dck_dm = pg.dockarea.Dock('dummy')
dck_fc = pg.dockarea.Dock('flow-chart')
dck_console = pg.dockarea.Dock('console')
pg_console = console.create_console()
dck_console.addWidget(pg_console)

mw.setCentralWidget(da)
da.addDock(dck_mt, position='left')
da.addDock(dck_fc, position='bottom', relativeTo=dck_mt)
da.addDock(dck_dm, position='right')
da.addDock(dck_console, position='below', relativeTo=dck_dm)


confg.main_fchart = fc = pg.flowchart.Flowchart()
dck_fc.addWidget(fc.widget())


plot_widget = pg.PlotWidget()
confg.dummy_plot_item_1 = plot_widget.plotItem
dck_dm.addWidget(plot_widget)
