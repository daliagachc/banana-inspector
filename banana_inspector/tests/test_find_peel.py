"""
9/17/21

diego.aliaga at helsinki dot fi
"""

#%%

from useful_scit.imps2.defs import *

from IPython import get_ipython


INTERACTIVE = False
_ipython = get_ipython()
# if interactiva ipython
if _ipython is not None:
    _magic = _ipython.magic
    # _magic( 'load_ext autoreload' )
    # _magic( 'autoreload 2' )
    _magic( 'gui qt5' )
    print('ipython')
    INTERACTIVE = True
    # noinspection PyStatementEffect
#     self.gui_qapp
# # if not interactive
else:
    # self.gui_qapp.exec_()
    print('not interactive')
    
    

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pyqtgraph.Qt.QtGui as QtGui
# import PyQt5.QtWidgets.QMainWindow
# from pyqtgraph.dockarea import *

from banana_inspector.plotters import BananaPlot

#%%
app = pg.mkQApp("Crosshair Example")
win = QtGui.QMainWindow()
win.resize(800,400)

bnn = BananaPlot.BananaPlot(win)

win.setCentralWidget(bnn)
win.show()
#%%
bnn.plot_example()
#%%
p1 = bnn.plot_item
vb = p1.vb
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)

p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)





# %%
class BnnPeelROI( pg.PolyLineROI ):
    def __init__( self , view_positions=None, pos = None  ):
        # print( args )
        if view_positions is None:
            view_positions = []
        pg.PolyLineROI.__init__(
                self , view_positions , pos = pos ,
                closed=True )
    
    def add_point( self , view_xy ):

        xys = self.get_roi_pol_coords()
        xys.append( view_xy )
        xys_kid = [ self.mapFromParent( xy ) for xy in xys ]
        
        self.setPoints( xys_kid )
    
    def get_roi_pol_coords( self ):
        """gets the ROI list of coords in the axis mapping"""
        pts = self.getState()[ 'points' ]
        pts = [ self.mapToParent( p ) for p in pts ]

        return pts
    
    
    def doubleClicked( self , segment , ev=None ,
                       pos=None ):  ## pos should be in this item's
        # coordinate system
        if ev != None:
            pos = segment.mapToParent( ev.pos() )
        elif pos != None:
            pos = pos
        else:
            raise Exception(
                    "Either an event or a position must be given." )
        h1 = segment.handles[ 0 ][ 'item' ]
        h2 = segment.handles[ 1 ][ 'item' ]
        
        i = self.segments.index( segment )
        h3 = self.addFreeHandle( pos , index=self.indexOfHandle( h2 ) )
        self.addSegment( h3 , h2 , index=i + 1 )
        segment.replaceHandle( h2 , h3 )

peel = BnnPeelROI( pos = [1527202602.7188394,-9.062239562428278] )


def mouseMoved(evt):
    global pos
    print('s')
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())


def get_roi_pol_coords( roi ):
    """gets the ROI list of coords in the axis mapping"""
    pts = roi.getState()[ 'points' ]
    pts = [ roi.mapToParent( p ) for p in pts ]
    xy_list = np.array( [ [ p.x() , p.y() ] for p in pts ] )
    return xy_list

def mouseClicked(evt):

    print('c')
    mc = evt[0]  ## using signal proxy turns original arguments into a tuple
    if not mc.double():
        return
    
    pos = mc.scenePos()
    viewPoint = vb.mapSceneToView( pos )
    peel.add_point( viewPoint)
  
    # xy = get_roi_pol_coords(r1)
    # r1.setAngle(0)
    # r1.setPos(0,0)
    # r1.setSize(1,1)

    # # new_x = mousePoint.x()
    # new_x = ppp.x()
    # # new_y = mousePoint.y()
    # new_y = ppp.y()
    # np.concatenate( (xy , [ [ new_x , new_y ] ]) , axis=0 )
    

    # hh = peel.handles[ -1 ][ 'item' ]
    #
    # h = peel.addFreeHandle( pos=[ new_x, new_y ] )
    # peel.addSegment( h , hh )
    
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())

proxy1 = pg.SignalProxy(bnn.plot_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

proxy2 = pg.SignalProxy(bnn.plot_item.scene().sigMouseClicked, rateLimit=60, slot=mouseClicked)

#%%





#%%
p1.addItem( peel )

#%%
# r1.addFreeHandle(.1, .1)

if not INTERACTIVE:
    app.exec_()