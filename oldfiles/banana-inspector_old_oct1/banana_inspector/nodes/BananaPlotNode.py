"""
9/16/21

diego.aliaga at helsinki dot fi
"""
import pyqtgraph_back
from pyqtgraph_back.flowchart.library.common import CtrlNode

from banana_inspector import shared_data
from banana_inspector.plotters.BananaPlot import BananaPlot

class BananaPlotNode( CtrlNode ):
    """
    - plots a particle size distribution in a new dock
    - it receives the data as xarray
    """
    nodeName = "BananaPlotNode"
    uiTemplate = [
            # ('sigma' , 'spin' ,
            #  { 'value': 1.0 , 'step': 1.0 , 'bounds': [ 0.0 , None ] }) ,
            # ('strength' , 'spin' ,
            #  { 'value' : 1.0 , 'dec': True , 'step': 0.5 , 'minStep': 0.01 ,
            #    'bounds': [ 0.0 , None ] }) ,
            # ('input_dir' , 'text' ,
            #  { 'value': './' })

        ('example data', 'check', {'checked': False})
            ]
    
    def __init__( self , name ):
        ## Define the input / output terminals available on this node
        terminals = {
                'dataIn': dict( io='in' ) ,
                'peel_roi': dict( io='in' ) ,
                # each terminal needs at least a name and
                'bnn_plot': dict( io='out' ) ,
                # to specify whether it is input or output
                }  # other more advanced options are available
        # as well..
        
        CtrlNode.__init__( self , name , terminals=terminals )
        
        # lets create a dock
        dock = pyqtgraph_back.dockarea.Dock(
                closable=True ,
                size=(100 , 1000) ,
                name=name
                )
        shared_data.dock_area.addDock( dock , position='right' )
        bnn_plot = BananaPlot( parent=dock )
        dock.addWidget( bnn_plot )
        
        # bnn_plot.plot_example()
        
        self.dock = dock
        self.bnn_plot = bnn_plot
        self.example_plotted = False
    
    
    def process( self ,
                 dataIn=None,
                 peel_roi=None ,
                 display=True ,
                 ):

        # CtrlNode has created self.ctrls, which is a dict containing {
        # ctrlName: widget}
        # sigma = self.ctrls[ 'sigma' ].value()
        # strength = self.ctrls[ 'strength' ].value()
        # text = self.ctrls['input_dir'].text()
        # output = dataIn - (
        #             strength * pg.gaussianFilter( dataIn , (sigma , sigma) ))
        
        # bnn_plot = BananaPlot()
        # dock_area = pg.dockarea
        # print( 'i am a bnn', text)
        # output = None
        # return { 'dataOut': output }

        if self.ctrls['example data'].isChecked():
            if self.example_plotted is False:
                self.bnn_plot.plot_example()
                self.example_plotted = True
        elif dataIn:
            self.bnn_plot.plot_from_sum_data( dataIn )

        if peel_roi:
            if peel_roi.plot_item != self.bnn_plot.plot_item:
                peel_roi.draw_me_in_plot(self.bnn_plot.plot_item)
        
        return {'bnn_plot':self.bnn_plot}