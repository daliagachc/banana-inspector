"""
9/14/21

diego.aliaga at helsinki dot fi
"""
# import banana_inspector.pyqtgraph.pyqtgraph.flowchart
# import pyqtgraph.flowchart.library as fclib
from IPython import get_ipython

INTERACTIVE = False
_ipython = get_ipython()
# if interactiva ipython
if _ipython is not None:
    _magic = _ipython.magic
    # _magic( 'load_ext autoreload' )
    # _magic( 'autoreload 2' )
    print('ipython')
    _magic('gui qt6')
    INTERACTIVE = True
    # noinspection PyStatementEffect
#     self.gui_qapp
# # if not interactive
else:
    # self.gui_qapp.exec_()
    print('not interactive')

from pyqtgraph_back.flowchart import Flowchart
from pyqtgraph_back.Qt import QtGui, QtCore
import pyqtgraph_back as pg
import pyqtgraph_back.dockarea
import numpy as np
import pyqtgraph_back.metaarray as metaarray
import PyQt5.QtWidgets
# from banana_inspector.docks.BananaPlot import BananaPlotNode
# from banana_inspector.docks.OpenFileNode import OpenFileNode
from banana_inspector import shared_data
from banana_inspector import pyqtgraph_bnn_extensions as exts


TITLE = "The Banana Inspector"

app = pg.mkQApp(TITLE)
exts.register_nodes()

## Create main window with grid layout
# win:PyQt5.QtWidgets.QMainWindow = QtGui.QMainWindow()
win: PyQt5.QtWidgets.QMainWindow = PyQt5.QtWidgets.QMainWindow()
win.setWindowTitle(TITLE)
win.setBaseSize(1200, 600)
# cw:PyQt5.QtWidgets.QWidget = QtGui.QWidget()
# cw:PyQt5.QtWidgets.QWidget = PyQt5.QtWidgets.QWidget()

dock_area = pyqtgraph_back.dockarea.DockArea()
shared_data.dock_area = dock_area
'''set the dock_area as fully global in the shared_data singleton'''

flow_chart_dock = pyqtgraph_back.dockarea.Dock(
    closable=True,
    size=(100, 800),
    name='flowchart control'
)

win.setCentralWidget(dock_area)
# layout:PyQt5.QtWidgets.QGridLayout = PyQt5.QtWidgets.QGridLayout()
# cw.setLayout(layout)


## Create flowchart, define input/output terminals
fc = Flowchart(terminals={
    'dataIn': {'io': 'in'},
    'dataOut': {'io': 'out'}
})

## Add flowchart control panel to the main window
flow_chart_dock.addWidget(fc.widget(), 0, 0, 2, 1)
dock_area.addDock(flow_chart_dock)

# %%


# %%
# fclib.registerNodeType(BananaPlotNode, [('Display',)])
# fclib.registerNodeType(OpenFileNode, [('Display',)])
# fclib.registerNodeType(UnsharpMaskNode, [('Image',)])


## Add two plot widgets
# pw1 = pg.PlotWidget()
# pw2 = pg.PlotWidget()
# layout.addWidget( pw1 , 0 , 1 )
# layout.addWidget( pw2 , 1 , 1 )

win.show()

# ## generate signal data to pass through the flowchart
# data = np.random.normal(size=1000)
# data[200:300] += 1
# data += np.sin(np.linspace(0, 100, 1000))
# data = metaarray.MetaArray(data, info=[
#     {'name': 'Time', 'values': np.linspace(0, 1.0, len(data))},
#     {}])
#
# ## Feed data into the input terminal of the flowchart
# fc.setInput(dataIn=data)

## populate the flowchart with a basic set of processing nodes.
## (usually we let the user do this)
# plotList = { 'Top Plot': pw1 , 'Bottom Plot': pw2 }

# pw1Node = fc.createNode( 'PlotWidget' , pos=(0 , -150) )
# pw1Node.setPlotList( plotList )
# pw1Node.setPlot( pw1 )

# pw2Node = fc.createNode( 'PlotWidget' , pos=(150 , -150) )
# pw2Node.setPlot( pw2 )
# pw2Node.setPlotList( plotList )

# fNode = fc.createNode( 'GaussianFilter' , pos=(0 , 0) )
# bnnNode = fc.createNode( 'BananaPlotNode' , pos=(100 , 100) )
# bnnNode = fc.createNode( 'OpenFileNode' , pos=(100 , 100) )


# fNode.ctrls[ 'sigma' ].setValue( 5 )
# fc.connectTerminals( fc[ 'dataIn' ] , fNode[ 'In' ] )
# fc.connectTerminals( fc[ 'dataIn' ] , pw1Node[ 'In' ] )
# fc.connectTerminals( fNode[ 'Out' ] , pw2Node[ 'In' ] )
# fc.connectTerminals( fNode[ 'Out' ] , fc[ 'dataOut' ] )


##### lets restore the status of the docks


if not INTERACTIVE:
    try:
        app.exec()

    except:
        app.exec_()

