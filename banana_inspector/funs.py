"""
6/17/21

diego.aliaga at helsinki dot fi
"""

import psd_ftools.funs as pfu
import numpy as np
import pandas as pd
from PyQt5 import QtCore
import xarray as xr
import pyqtgraph_back as pg

def open_sum( sum_path ):
    ds = pfu.open_sum2ds( sum_path )
    return ds


def get_treated_da( ds ):
    # todo make sure the da is better
    # da should not have nans
    # we use log10
    da = ds[ pfu.DNDLDP ]
    rt = 5  # averaging time in minutes
    len_ldp = 0.0646  # delta lDp
    
    da1 = da.dropna( 'time' , how='all' ).dropna( 'Dp' , how='all' )
    dr = da1.resample( { 'time': f'{rt}T' } , label='left' ).mean()
    
    dr[ 'time' ] = dr[ 'time' ] + pd.Timedelta( rt / 2 , 'minutes' )
    
    dr[ 'lDp' ] = np.log10( dr[ 'Dp' ] )
    
    dr1 = dr.swap_dims( { 'Dp': 'lDp' } )
    
    drange = np.arange( dr[ 'lDp' ].min() , dr[ 'lDp' ].max() , len_ldp / 4 )
    
    dr2 = dr1.interp( { 'lDp': drange } )
    
    dr2 = dr2.coarsen( { 'lDp': 4 } , boundary='trim').mean()
    dr2[ 'lDp' ] = dr2[ 'lDp' ] + len_ldp / 2
    
    dr2 = dr2.interpolate_na( dim='time' , limit=2 )
    
    # assert dr2.isnull().sum().item() == 0
    
    dr2 = dr2.where( dr2 > 0 , -10 )

    dr3 = dr2.transpose( 'time' , 'lDp' )
    
    return dr3


def infer_interval_breaks( coord , axis=0 , check_monotonic=False ):
    """
    >>> infer_interval_breaks(np.arange(5))
    array([-0.5,  0.5,  1.5,  2.5,  3.5,  4.5])
    >>> infer_interval_breaks([[0, 1], [3, 4]], axis=1)
    array([[-0.5,  0.5,  1.5],
           [ 2.5,  3.5,  4.5]])
    """
    coord = np.asarray( coord )
    
    if check_monotonic and not _is_monotonic( coord , axis=axis ):
        raise ValueError( "The input coordinate is not sorted in increasing "
                          "order along axis %d. This can lead to unexpected "
                          "results. Consider calling the `sortby` method on "
                          "the input DataArray. To plot data with categorical "
                          "axes, consider using the `heatmap` function from "
                          "the `seaborn` statistical plotting library." % axis )
    
    deltas = 0.5 * np.diff( coord , axis=axis )
    if deltas.size == 0:
        deltas = np.array( 0.0 )
    first = np.take( coord , [ 0 ] , axis=axis ) - np.take( deltas , [ 0 ] ,
                                                            axis=axis )
    last = np.take( coord , [ -1 ] , axis=axis ) + np.take( deltas , [ -1 ] ,
                                                            axis=axis )
    trim_last = tuple(
            slice( None , -1 ) if n == axis else slice( None ) for n in
            range( coord.ndim ) )
    return np.concatenate( [ first , coord[ trim_last ] + deltas , last ] ,
                           axis=axis )


def _is_monotonic( coord , axis=0 ):
    """
    >>> _is_monotonic(np.array([0, 1, 2]))
    True
    >>> _is_monotonic(np.array([2, 1, 0]))
    True
    >>> _is_monotonic(np.array([0, 2, 1]))
    False
    """
    if coord.shape[ axis ] < 3:
        return True
    else:
        n = coord.shape[ axis ]
        delta_pos = coord.take( np.arange( 1 , n ) , axis=axis ) >= coord.take(
                np.arange( 0 , n - 1 ) , axis=axis )
        delta_neg = coord.take( np.arange( 1 , n ) , axis=axis ) <= coord.take(
                np.arange( 0 , n - 1 ) , axis=axis )
        return np.all( delta_pos ) or np.all( delta_neg )


def set_secs_dim( da ):
    da1 = da
    if 'secs' not in da1.dims:
        if 'secs' not in list(da1.coords):
            _dif = (da1[ 'time' ] - np.datetime64( '1970' ))
            da1[ 'secs' ] = _dif / np.timedelta64( 1 , 's' )
        
        da1 = da1.swap_dims( { 'time': 'secs' } )
    
    assert 'secs' in da1.dims
    
    return da1


def gauss_scipy( da , xpixel , ypixel ):
    from scipy.ndimage import gaussian_filter
    res = gaussian_filter( da , (ypixel , xpixel) )
    nda = xr.ones_like( da ) * res
    return nda


def gauss_astro( da , xpixel , ypixel ):
    if xpixel == 0:
        xpixel = .0001
    if ypixel == 0:
        ypixel = .0001
    
    from astropy.convolution import Gaussian2DKernel
    from astropy.convolution import convolve
    kernel = Gaussian2DKernel( x_stddev=xpixel , y_stddev=ypixel )
    res = convolve( da , kernel )
    nda = xr.ones_like( da ) * res
    return nda


def get_darray_of_interest_from_polyxy( da , poly ):
    da = set_secs_dim( da )
    mask = get_darray_of_interest_mask_from_polyxy( da , poly )
    da1 = da.where( mask )
    
    return da1

def get_darray_of_interest_mask_from_polyxy( da , poly ):
    da = set_secs_dim( da )
    from matplotlib.path import Path
    
    path = Path( poly , closed=False )
    
    # qr = ROI.parentBounds()
    
    top = poly[ : , 1 ].max()
    bot = poly[ : , 1 ].min()
    
    right = poly[ : , 0 ].max()
    left = poly[ : , 0 ].min()
    
    # top = np.max( [ qr.bottom() , qr.top() ] )
    # bot = np.min( [ qr.bottom() , qr.top() ] )
    # right = qr.right()
    # left = qr.left()
    
    if 'secs' not in da.dims:
        da = set_secs_dim( da )
    
    da_slice = da.loc[
        { 'secs': slice( left , right ) , 'lDp': slice( bot , top ) } ]
    # da.loc[{'time':slice(np.datetime64(left,'s'),np.datetime(right,'s'))}]
    
    # path = Path(r2.getState()['points'])
    
    _dp = xr.ones_like( da_slice ) * da_slice[ 'lDp' ]
    _se = xr.ones_like( da_slice ) * da_slice[ 'secs' ]
    
    _co = xr.concat( [ _se , _dp ] , 'xy' )
    
    xy = _co.transpose( 'lDp' , 'secs' , 'xy' ).values

    # noinspection PyUnresolvedReferences
    a , b , c = xy.shape

    # noinspection PyUnresolvedReferences
    mask = path.contains_points( xy.reshape( a * b , c ) )
    mask = mask.reshape( a , b )
    
    xmask = xr.zeros_like( da_slice ) + mask
    
    return xmask

def set_image_data( da , img:pg.ImageItem , autoLevels ):
    d0 , d1 , t00 , t11 = get_darray_bounds( da )
    da = da.where( da > 1 , 1 )
    lda = np.log10( da )
    # lda = lda.where(lda>0,0)
    data = lda.values
    img.setImage( data , autoLevels=autoLevels )
    width = t11 - t00
    height = d1 - d0
    rect = QtCore.QRectF( t00 , d0 , width , height )
    img.setRect( rect )
    
    # %%

def open_darray( pp ):
    ip_darray = open_sum( pp )
    
    ip_darray = get_treated_da( ip_darray )
    
    da = set_secs_dim( ip_darray )
    da[ 'tempK' ] = xr.zeros_like( da[ 'secs' ] ) + 273
    da[ 'presP' ] = xr.zeros_like( da[ 'secs' ] ) + 532000

    da1 = da.transpose( 'secs' , 'lDp' )
    
    return da1

def get_darray_bounds( da: xr.DataArray ):
    """get the bounds for the darray"""
    assert 'time' in list( da.coords )
    assert 'lDp' in list( da.coords )
    
    t0 , t1 = infer_interval_breaks( da[ 'time' ] )[ [ 0 , -1 ] ]
    d0 , d1 = infer_interval_breaks( da[ 'lDp' ] )[ [ 0 , -1 ] ]
    t00 = (t0 - np.datetime64( '1970' )) / np.timedelta64( 1 , 's' )
    t11 = (t1 - np.datetime64( '1970' )) / np.timedelta64( 1 , 's' )
    return d0 , d1 , t00 , t11
    
    
    # p1 = self.gui_glw_a.addPlot(
    #         title="log( dN /dlog(Dp) )" ,
    #         axisItems={ 'bottom': time_axis } )
    
    # self.gui_plot_a = p1
    
    # self.gui_plot_a.setLogMode( x=None , y=True )
    
    # self.gui_img_a = pg.ImageItem()
    #
    # self.gui_plot_a.addItem( self.gui_img_a )
    #
    # hist = pg.HistogramLUTItem()
    # hist.gradient.loadPreset( 'viridis' )
    # hist.setImageItem( self.gui_img_a )
    # self.gui_glw_a.addItem( hist )
    #
    # self.gui_hist_a = hist
    #
    # pts = [ [ 1.52725508e+09 , -7.70968700e+00 ] ,
    #         [ 1.52725136e+09 , -8.00565669e+00 ] ,
    #         [ 1.52725009e+09 , -8.35900826e+00 ] ,
    #         [ 1.52727887e+09 , -8.35296807e+00 ] ,
    #         [ 1.52727831e+09 , -8.00565670e+00 ] ,
    #         [ 1.52728016e+09 , -7.71155135e+00 ] ]
    #
    # self.gui_ROI_a = pg.PolyLineROI( pts , pen=(6 , 9) , closed=True )
    #
    # self.gui_plot_a.addItem( self.gui_ROI_a )
    
    # set grid
    # Fix Axes ticks and grid
    #   - there is a bug in this grid thing
    # grid_opacity = .5
    # for key in self.gui_plot_a.axes:
    #     ax = self.gui_plot_a.getAxis( key )
    #     ax.setGrid( grid_opacity * 255 )
    #
    #     # Set the grid opacity
    #     # if grid_is_visible:
    #     #     ax.setGrid( grid_opacity * 255 )
    #     # else:
    #     #     ax.setGrid( False )
    #
    #     # Fix Z value making the grid on top of the image
    #     ax.setZValue( 1 )