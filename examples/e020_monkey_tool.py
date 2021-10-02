'''simplest possible app
also the main lauout for the application
maybe it shold be a test at some point\
'''

import pyqtgraph as pg
import pyqtgraph.dockarea
import pyqtgraph.flowchart
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

import banana_inspector.util.console
import banana_inspector.util.log_bnn as lg
from banana_inspector import confg
import pyqtgraph.parametertree


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
mw.resize(500, 800)

confg.dock_area = da = pg.dockarea.DockArea()

dck_mt = pg.dockarea.Dock('mnk-tool')

dck_fc = pg.dockarea.Dock('flow-chart')
fc = pyqtgraph.flowchart.Flowchart()
fw = fc.widget()
dck_fc.addWidget(fw)
confg.main_fchart = fc

mw.setCentralWidget(da)
da.addDock(dck_mt, position='left')
da.addDock(dck_fc, position='bottom', relativeTo=dck_mt)

mw.show()


p = confg.par_tree


t = pyqtgraph.parametertree.ParameterTree()

#todo fix size issue

# dck_mt.addWidget(t)
mw.setCentralWidget(da)
t.setParameters(p)

dck_mt.addWidget(t)


def save_main_window():
    #probably we dont need this
    pass
    geo = confg.main_window.geometry()
    x = geo.x()
    y = geo.y()
    w = geo.width()
    h = geo.height()
    # return  confg.main_window.saveState()
    return (x,y,w,h)


def save_dock_area():
    pass
    da = confg.dock_area
    s = da.saveState()
    lg.ger.debug(s)
    return s


def save_flow_chart():
    pass
    fc = confg.main_fchart

    s = fc.saveState()
    lg.ger.debug(s)
    return s


# def get_file():
#     w = QtWidgets.QFileDialog()
#     w.show()


def save_project():
    from pyqtgraph.configfile import  writeConfigFile
    # get_file()
    smw = save_main_window()
    sda = save_dock_area()
    sfc = save_flow_chart()

    sd = dict()
    sd['main_window'] = smw
    sd['dock_area'] = sda
    sd['flow_chart'] = sfc

    # sd = sfc

    file = confg.par_tree['file proj']



    # lg.ger.debug(sd)
    writeConfigFile(sd,file)



def open_project():
    from pyqtgraph.configfile import  readConfigFile
    file = confg.par_tree['file proj']
    lg.ger.debug(file)
    sd = readConfigFile(file)

    smw = sd['main_window']
    x,y,w,h = smw
    rec = QtCore.QRect(x,y,w,h)
    confg.main_window.setGeometry(rec)

    sda = sd['dock_area']
    confg.dock_area.restoreState(sda)

    sfc = sd['flow_chart']
    confg.main_fchart.restoreState(sfc)

    # lg.ger.debug(st)



p.param('save project').sigActivated.connect(save_project)
p.param('open project').sigActivated.connect(open_project)


p['project dir'] = '/tmp/'
p['file proj'] = '/tmp/ff.txt'

if INT is False:
    pg.exec()
if INT is True:
    pass
    confg.main_window.show()
