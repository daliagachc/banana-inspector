"""
6/18/21

diego.aliaga at helsinki dot fi
"""
import os

import pandas as pd
import numpy as np
import funs as fu
import xarray as xr
from scipy.optimize import curve_fit


class AppearanceModeFit:
    """this is the class to do the fit"""
    
    def __init__( self , raw_darray, smooth_darray , roi_points ,
                  appearance_fit_save_dir ):
        # @formatter:off
        # noinspection PyTypeChecker
        self.df      :   pd.DataFrame    =   None
        self.df_mandatory_cols  = ['x','y','x0','y0']
        self.par_order          = ['x0' , 'L',  'k', 'D']
        self.par_order_guess    = ['x0_'    , 'L_'  ,  'k_' , 'D_'  ]
        self.par_order_mx       = ['x0mx'   , 'Lmx' ,  'kmx', 'Dmx' ]
        self.par_order_mn       = ['x0mn'   , 'Lmn' ,  'kmn', 'Dmn' ]
        self.appearance_fit_save_dir = appearance_fit_save_dir
        self.save_path = None
        self.roi_points = roi_points
        self.method_name = 'appearance_method'
        self.sdarray = None # smooth array
        self.rarray = None # raw array
        # @formatter:off

        self.sdarray = fu.get_darray_of_interest_from_polyxy(smooth_darray,roi_points)
        self.rdarray = fu.get_darray_of_interest_from_polyxy(raw_darray,roi_points)
        self.df = self.get_fit_pars_df()
        self.df = self.mode_fit_df()
        
        # self.save_fit_df()
        
    def save_fit_df(self, ip_mode , sign ):
        self.save_path = self._get_save_path( ip_mode , sign )
        self._save_df()
        
    def _get_save_path(self, ip_mode , sign):
        arr = self.roi_points
        secs = arr[ : , 0 ]
        mean_secs = secs.mean()
        dt = pd.to_datetime( mean_secs , unit='s' )
        dt = dt.strftime( '%Y-%m-%dT%H.csv' )
        dt = f'{self.method_name}_{ip_mode}_{sign}_{dt}'
        save_path = os.path.join(self.appearance_fit_save_dir,dt)
        return save_path
    
    def _save_df(self):
        self.df.to_csv(self.save_path)
        
    @staticmethod
    def fit_function( x , x0 , L,  k, D):
        # x0 , L,  k, D
        fun = (
                      L * (1 + np.exp( -k * (x - x0) )) ** (-1)
              ) + D
        return fun
    
    def get_fit_pars_df( self ):
    
        assert 'secs' in self.sdarray.dims
        assert 'lDp' in self.sdarray.dims
        assert 'secs' in self.rdarray.dims
        assert 'lDp' in self.rdarray.dims
        
        # sdf.index = lDP
        # sdf.columns = secs
        # sdf values = log10 (dNdlDp)
        sdf = self.sdarray.to_series().unstack( 'secs' )
        rdf = self.rdarray.to_series().unstack( 'secs' )
        
        assert np.all(sdf.index == rdf.index)
        
        dic = { }
        for lDp , v in sdf.iterrows():
            vv = v.dropna()
            x_secs = vv.index.to_numpy()  # np.array
            y_val = vv.values
            dic[ lDp ] = self.get_fit_pars( x_secs , y_val )
            
            rvv = rdf.loc[lDp].dropna()
            rx_secs = rvv.index.to_numpy()
            ry_val = rvv.values
            dic[ lDp ]['x_raw'] = rx_secs
            dic[ lDp ]['y_raw'] = ry_val
        dff = pd.DataFrame( dic ).T
        dff.index.name = sdf.index.name
        return dff
    
    @staticmethod
    def get_fit_pars( secs , val ):
        i_mx = np.argmax( val )
        i_mn = np.argmin( val )
    
        imax = max( [ i_mx , i_mn ] )
        imin = min( [ i_mx , i_mn ] )
    
        x = secs[ imin:imax ]
        y = val[ imin:imax ]
    
        D_ = val[ i_mn ]
        L_ = val[ i_mx ] - D_
    
        delta_secs = (secs[ i_mx ] - secs[ i_mn ])
        x0_ = delta_secs / 2 + secs[ i_mn ]
    
        k_ = 1 / delta_secs
    
        Dmn = D_ / 1.1
        Dmx = D_ * 1.1
    
        Lmn = L_ / 1.1
        Lmx = L_ * 1.1
    
        x0mn = secs[ i_mn ]
        x0mx = secs[ i_mx ]
    
        kmn = k_ / 500
        kmx = k_ * 500
    
        dout = { 'D_'  : D_ ,
                 'Dmn' : Dmn ,
                 'Dmx' : Dmx ,
                 #
                 'L_'  : L_ ,
                 'Lmn' : Lmn ,
                 'Lmx' : Lmx ,
                 #
                 'x0_' : x0_ ,
                 'x0mn': x0mn ,
                 'x0mx': x0mx ,
                 #
                 'k_'  : k_ ,
                 'kmn' : kmn ,
                 'kmx' : kmx ,
                 'x'   : x ,
                 'y'   : y ,
                 }
    
        return dout

    def mode_fit_df( self ):
        dff = self.df
        new_dff = { }
        for lDp , row in dff.iterrows():
            res = self.fit_curve_from_row( row )
            for k,v in res.items():
                row[k] = v
            new_dff[ lDp ] = row
        
        new_dff = pd.DataFrame( new_dff ).T
        new_dff.index.name = dff.index.name
        
        return new_dff

    def fit_curve_from_row( self, row  ):

        # par_order = x0 , L,  k, D

        p0 = [row[k] for k in self.par_order_guess]
        
        bmn = [row[k] for k in self.par_order_mn]
    
        bmx = [row[k] for k in self.par_order_mx]
        
        x_ = row[ 'x' ]
        y_ = row[ 'y' ]
        
        (x0 , L,  k, D) , corr = curve_fit( self.fit_function ,
                                            x_ , y_ ,
                                            p0=p0 ,
                                            bounds=[ bmn , bmx ] )
        res = {
                'x0' : x0,
                'L' : L,
                'k' : k,
                'D' : D,
                'corr' : corr
                }
        return res
