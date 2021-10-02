'''simplest possible app
also the main lauout for the application
maybe it shold be a test at some point\
'''

import pyqtgraph as pg
import pyqtgraph.console
import pyqtgraph.dockarea
import pyqtgraph.flowchart
from pyqtgraph.Qt import QtWidgets

import banana_inspector.util.log_bnn as lg
from banana_inspector import confg
import banana_inspector.util.console

lg.ger.setLevel(10)


def set_int():
    from IPython import get_ipython
    try:
        get_ipython().magic('gui qt5')
        INT = True
        lg.ger.info('interactive')
        pass
        # INT = False

    except:
        INT = False
        lg.ger.info('not interactive')
    return INT


# INT = set_int()
INT = False

app = pg.mkQApp()



confg.main_window = mw = QtWidgets.QMainWindow()
mw.resize(1000,800)

confg.dock_area = da = pg.dockarea.DockArea()
confg.main_fchart = fc = pg.flowchart.Flowchart()
dck_mt = pg.dockarea.Dock('mnk-tool')
dck_dm = pg.dockarea.Dock('dummy')
dck_fc = pg.dockarea.Dock('flow-chart')
dck_console = pg.dockarea.Dock('console')
pg_console = banana_inspector.util.console.create_console()
dck_console.addWidget(pg_console)



mw.setCentralWidget(da)
da.addDock(dck_mt, position='left')
da.addDock(dck_fc, position='bottom', relativeTo=dck_mt)
da.addDock(dck_dm, position='right')
da.addDock(dck_console, position='below', relativeTo=dck_dm)

mw.show()

if INT is False:
    pg.exec()
if INT is True:
    pass
    confg.main_window.show()
