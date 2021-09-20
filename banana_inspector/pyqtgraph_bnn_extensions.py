"""
9/16/21

diego.aliaga at helsinki dot fi
"""
from pyqtgraph import QtCore
from pyqtgraph import QtGui
import PyQt5
from pyqtgraph.widgets.SpinBox import SpinBox
from pyqtgraph.widgets.ColorButton import ColorButton
from pyqtgraph.WidgetGroup import WidgetGroup
from pyqtgraph.flowchart import Node
import pyqtgraph.flowchart.library as fclib

from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

def generateUi( opts ):
    """Convenience function for generating common UI types"""
    widget = QtGui.QWidget()
    l = QtGui.QFormLayout()
    l.setSpacing( 0 )
    widget.setLayout( l )
    ctrls = { }
    row = 0
    for opt in opts:
        if len( opt ) == 2:
            k , t = opt
            o = { }
        elif len( opt ) == 3:
            k , t , o = opt
        else:
            raise Exception(
                "Widget specification must be (name, type) or (name, type, {opts})" )
        
        ## clean out these options so they don't get sent to SpinBox
        hidden = o.pop( 'hidden' , False )
        tip = o.pop( 'tip' , None )
        
        if t == 'intSpin':
            w = QtGui.QSpinBox()
            if 'max' in o:
                w.setMaximum( o[ 'max' ] )
            if 'min' in o:
                w.setMinimum( o[ 'min' ] )
            if 'value' in o:
                w.setValue( o[ 'value' ] )
        elif t == 'doubleSpin':
            w = QtGui.QDoubleSpinBox()
            if 'max' in o:
                w.setMaximum( o[ 'max' ] )
            if 'min' in o:
                w.setMinimum( o[ 'min' ] )
            if 'value' in o:
                w.setValue( o[ 'value' ] )
        elif t == 'spin':
            w = SpinBox()
            w.setOpts( **o )
        elif t == 'check':
            w = QtGui.QCheckBox()
            if 'checked' in o:
                w.setChecked( o[ 'checked' ] )
        elif t == 'combo':
            w = QtGui.QComboBox()
            for i in o[ 'values' ]:
                w.addItem( i )
        elif t == 'text':
            w = QtGui.QLineEdit()
            w.setText( o[ 'value' ] )
            
        # elif t == 'colormap':
        # w = ColorMapper()
        elif t == 'color':
            w = ColorButton()
        else:
            raise Exception( "Unknown widget type '%s'" % str( t ) )
        
        if tip is not None:
            w.setToolTip( tip )
        w.setObjectName( k )
        l.addRow( k , w )
        if hidden:
            w.hide()
            label = l.labelForField( w )
            label.hide()
        
        ctrls[ k ] = w
        w.rowNum = row
        row += 1
    group = WidgetGroup( widget )
    return widget , group , ctrls


class CtrlNodeExt( Node ):
    """Abstract class for nodes with auto-generated control UI
    This class was extended by bnn-inspection"""
    
    sigStateChanged = QtCore.Signal( object )
    
    def __init__( self , name , ui=None , terminals=None ):
        if terminals is None:
            terminals = { 'In' : { 'io': 'in' } ,
                          'Out': { 'io': 'out' , 'bypass': 'In' } }
        Node.__init__( self , name=name , terminals=terminals )
        
        if ui is None:
            if hasattr( self , 'uiTemplate' ):
                ui = self.uiTemplate
            else:
                ui = [ ]
        
        self.ui , self.stateGroup , self.ctrls = generateUi( ui )
        self.stateGroup.sigChanged.connect( self.changed )
    
    def ctrlWidget( self ):
        return self.ui
    
    def changed( self ):
        self.update()
        self.sigStateChanged.emit( self )
    
    def process( self , In , display=True ):
        out = self.processData( In )
        return { 'Out': out }
    
    def saveState( self ):
        state = Node.saveState( self )
        state[ 'ctrl' ] = self.stateGroup.state()
        return state
    
    def restoreState( self , state ):
        Node.restoreState( self , state )
        if self.stateGroup is not None:
            self.stateGroup.setState( state.get( 'ctrl' , { } ) )
    
    def hideRow( self , name ):
        w = self.ctrls[ name ]
        l = self.ui.layout().labelForField( w )
        w.hide()
        l.hide()
    
    def showRow( self , name ):
        w = self.ctrls[ name ]
        l = self.ui.layout().labelForField( w )
        w.show()
        l.show()


def register_nodes():
    '''registers all the nodes in the nodes folder.
    the name of the node class should by the same as the module name'''
    import banana_inspector.nodes as nodes
    import glob
    from importlib import import_module
    node_path = nodes.__path__[0]
    names = glob.glob1(node_path,'*Node.py')
    n2 = [n[:-3] for n in names]
    node_klasses = []
    for n in n2:
        mod = import_module(f'banana_inspector.nodes.{n}')
        k = getattr(mod,n)
        fclib.registerNodeType( k , [ ('Display' ,) ] )