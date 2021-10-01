"""
9/14/21

diego.aliaga at helsinki dot fi
"""
from pyqtgraph_back import GraphicsLayoutWidget
import pyqtgraph_back as pg
from .. import shared_data
from ..funs import set_image_data , open_darray

from .. import funs

# from ..pyqtgraph_bnn_extensions import CtrlNode
# import pyqtgraph as pg


class BananaPlot( GraphicsLayoutWidget ):
    
    def __init__( self , parent , **kargs ):
        super().__init__( parent=parent , **kargs )
        
        # self.time_axis = pg.DateAxisItem( utcOffset=0 )
        
        axisItems = { 'bottom': pg.DateAxisItem( utcOffset=0 ) }
        plot_item: pg.PlotItem = pg.PlotItem( axisItems=axisItems )
        
        plot_item.setTitle( "log( dN /dlog(Dp) )" )
        # plot_item.setAxisItems()
        plot_item.setLogMode( x=None , y=True )
        
        image_item = pg.ImageItem()
        plot_item.addItem( image_item )
        
        hist = pg.HistogramLUTItem()
        hist.axis.setLogMode( True )
        hist.gradient.loadPreset( 'viridis' )
        hist.setImageItem( image_item )
        
        self.ci.addItem( hist )
        self.ci.addItem( plot_item )
        
        self.image_item = image_item
        self.plot_item = plot_item
    
    
    def plot_example( self ):
        # %%
        from .. import example_data
        import os.path
        path = example_data.__path__[ 0 ]
        p1 = os.path.join( path , 'lev2_NAISp20180525np.sum' )
        # p1 = 'example_data/lev2_NAISp20180525np.sum'
        da1 = open_darray( p1 )
        shared_data.banana_data = da1
        set_image_data( da1 , self.image_item , autoLevels=True )

    
    
    def plot_from_data( self , da1 ):
        # %%
        # from .. import example_data
        # import os.path
        # path = example_data.__path__[ 0 ]
        # p1 = os.path.join( path , 'lev2_NAISp20180525np.sum' )
        # p1 = 'example_data/lev2_NAISp20180525np.sum'
        # da1 = open_darray( p1 )
        shared_data.banana_data = da1
        set_image_data( da1 , self.image_item , autoLevels=True )

    def plot_from_sum_data( self , da ):
        import xarray as xr
        # %%
        # from .. import example_data
        # import os.path
        # path = example_data.__path__[ 0 ]
        # p1 = os.path.join( path , 'lev2_NAISp20180525np.sum' )
        # p1 = 'example_data/lev2_NAISp20180525np.sum'
        # da1 = open_darray( p1 )
        ip_darray = funs.get_treated_da( da )

        da = funs.set_secs_dim( ip_darray )
        da[ 'tempK' ] = xr.zeros_like( da[ 'secs' ] ) + 273
        da[ 'presP' ] = xr.zeros_like( da[ 'secs' ] ) + 532000

        da1 = da.transpose( 'secs' , 'lDp' )
        set_image_data( da1 , self.image_item , autoLevels=False )

