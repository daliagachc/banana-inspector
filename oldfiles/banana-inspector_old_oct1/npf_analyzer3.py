"""
6/16/21

diego.aliaga at helsinki dot fi
"""

# noinspection PyUnresolvedReferences
import os.path

# noinspection PyUnresolvedReferences
import psd_ftools.funs as pfu
import pyqtgraph_back as pg
import funs as fu

# noinspection PyUnresolvedReferences
from pyqtgraph_back.Qt import QtCore , QtGui
# noinspection PyUnresolvedReferences
import numpy as np
# noinspection PyUnresolvedReferences
import pandas as pd
# noinspection PyUnresolvedReferences
import xarray as xr
import pyqtgraph_back.dockarea
import pyqtgraph_back.console
import pyqtgraph_back.widgets.SpinBox
import AppearanceModeFit as Amf



class GuiNpf:
    def __init__( self ):
        # VARIABLES
        
        ## colors
        self.appea_color = ( 200 , 0 , 200 )
        
        ## general area parameters
        self.gui_qapp = pg.mkQApp( 'NPF event analyzer' )
        # noinspection PyUnresolvedReferences
        self.gui_win = QtGui.QMainWindow()
        self.gui_area = pyqtgraph_back.dockarea.DockArea()
        
        ## docks
        self.gui_dock_a = pyqtgraph_back.dockarea.Dock('dock a')
        self.gui_dock_b = pyqtgraph_back.dockarea.Dock('dock b')
        self.gui_dock_c = pyqtgraph_back.dockarea.Dock('dock c')
        self.gui_dock_d = pyqtgraph_back.dockarea.Dock('dock d')
        self.gui_dock_e = pyqtgraph_back.dockarea.Dock('dock e')
        
        ## graphical layouts widgets
        self.gui_glw_a = pg.GraphicsLayoutWidget()
        self.gui_glw_b = pg.GraphicsLayoutWidget()
        self.gui_glw_c = pg.GraphicsLayoutWidget()
        self.gui__lw_d = pg.LayoutWidget()
        self.gui__lw_e = pg.LayoutWidget()
        
        self.gui_scroll_c = QtGui.QScrollArea()
        
        ## plot items
        self.gui_plot_a = None
        self.gui_plot_b = None

        self.appea_curve = None
        
        self.gui_plot_c_list = []
        
        # plot a variables
        self.gui_hist_a = None
        self.gui_img_a = None
        # noinspection PyTypeChecker
        self.gui_ROI_a: pg.PolyLineROI = None
        
        # console
        # noinspection PyTypeChecker
        self.gui_console: pyqtgraph_back.console.ConsoleWidget = None
        
        # gui buttons
        # to avoid annoying message
        QtGui.QPushButton = QtGui.QPushButton
        self.gui_but_fit_mmd_mconc = QtGui.QPushButton( 'fit max concen' )
        self.gui_but_fit_mmd_appea = QtGui.QPushButton( 'fit appearance' )
        self.gui_but_fit_mmd_mmode = QtGui.QPushButton( 'fit main mode' )
        
        self.gui_but_plot_mmd_mconc = QtGui.QPushButton( 'plot max concen' )
        self.gui_but_plot_mmd_appea = QtGui.QPushButton( 'plot appearance' )
        self.gui_but_plot_mmd_mmode = QtGui.QPushButton( 'plot main mode' )
        
        self.gui_but_save_mmd_mconc = QtGui.QPushButton( 'save max concen' )
        self.gui_but_save_mmd_appea = QtGui.QPushButton( 'save appearance' )
        self.gui_but_save_mmd_mmode = QtGui.QPushButton( 'save main mode' )
        
        self.gui_but_save_roi = QtGui.QPushButton( 'save ROI' )
        
        self.gui_combo_open = QtGui.QComboBox()
        
        
        # spins
        _sb = pyqtgraph_back.widgets.SpinBox.SpinBox
        # noinspection PyTypeChecker
        self.gui_spin_dp_mn: _sb = None
        # noinspection PyTypeChecker
        self.gui_spin_dp_mx: _sb = None
        # noinspection PyTypeChecker
        self.gui_spin_smooth_x: _sb = None
        # noinspection PyTypeChecker
        self.gui_spin_smooth_y: _sb = None
        
        # ion or particle (ip) parameters
        # noinspection PyTypeChecker
        self.ip_darray: xr.DataArray = None
        # ion or particle mode: "ion" "particle"
        # noinspection PyTypeChecker
        self.ip_mode: str = None  # "ion" "particle"
        self.ip_sign: str = None # "pos" "neg" "neu"
        
        """prject root path"""
        self.project_path_root = None
        """project region of interest (roi)"""
        self.project_path_roi = None
        """project appearance dir"""
        self.project_path_appearance = None
        
        # FIT object
        # noinspection PyTypeChecker
        self.fits_AMF : Amf.AppearanceModeFit = None # appearance mode fit
        
        # INIT METHODS
        
        # init guis
        self.init_gui_general_area()
        self.init_gui_docks()
        self.init_gui_buttons()
        self.init_gui_spins()
        
        # init plots
        self.init_gui_plot_a()
        self.init_gui_plot_b()
        
        # init console
        self.init_gui_console_e()
        
        # add pi size dist
        # self.set_ip_mode(ip_mode)
        # self.set_ip_data_array( ip_darray )
        # self.plot_ip_size_dist()
        
        # launch qapp
        self.launch_qapp()
    
    def init_gui_general_area( self ):
        pg.setConfigOptions( imageAxisOrder='row-major' )
        
        # win = pg.GraphicsLayoutWidget()
        
        # app = pg.mkQApp( "DockArea Example" )
        
        self.gui_win.setCentralWidget( self.gui_area )
        self.gui_win.resize( 1600 , 800 )
        self.gui_win.setWindowTitle( 'pyqtgraph example: Image Analysis' )
        self.gui_win.show()
    
    def init_gui_docks( self ):
        ls = [ self.gui_dock_a ,
               self.gui_dock_b ,
               self.gui_dock_c ,
               self.gui_dock_d ,
               self.gui_dock_e ,
               ]

        self.gui_scroll_c.setWidget(self.gui_glw_c)
        self.gui_scroll_c.setWidgetResizable( True )
        # self.gui_scroll_c.setFixedHeight( 400 )
        
        gs = [ self.gui_glw_a ,
               self.gui_glw_b ,
               self.gui_scroll_c ,
               self.gui__lw_d ,
               self.gui__lw_e ,
               ]
        
        for l , g in zip( ls , gs ):
            self.gui_area.addDock( l )
            l.addWidget( g )
        
        state = { 'main' : ('horizontal' ,
                            [ ('vertical' ,
                               [ ('dock' , 'dock a' , { }) ,
                                 ('horizontal' ,
                                  [ ('tab' , [ ('dock' , 'dock e' , { }) ,
                                               ('dock' , 'dock d' , { }) ] ,
                                     { 'index': 1 }) ,
                                    ('dock' , 'dock b' , { }) ] ,
                                  { 'sizes': [ 529 , 414 ] }) ] ,
                               { 'sizes': [ 421 , 427 ] }) ,
                              ('dock' , 'dock c' , { }) ] ,
                            { 'sizes': [ 950 , 483 ] }) ,
                  'float': [ ] }
        
        self.gui_area.restoreState( state )
    
    def init_gui_plot_a( self ):
        time_axis = pg.DateAxisItem( utcOffset=0 )
        
        p1 = self.gui_glw_a.addPlot(
                title="log( dN /dlog(Dp) )" ,
                axisItems={ 'bottom': time_axis } )
        
        self.gui_plot_a = p1
        
        self.gui_plot_a.setLogMode( x=None , y=True )
        
        self.gui_img_a = pg.ImageItem()
        
        self.gui_plot_a.addItem( self.gui_img_a )
        
        hist = pg.HistogramLUTItem()
        hist.gradient.loadPreset( 'viridis' )
        hist.setImageItem( self.gui_img_a )
        self.gui_glw_a.addItem( hist )
        
        self.gui_hist_a = hist
        
        pts = [ [ 1.52725508e+09 , -7.70968700e+00 ] ,
                [ 1.52725136e+09 , -8.00565669e+00 ] ,
                [ 1.52725009e+09 , -8.35900826e+00 ] ,
                [ 1.52727887e+09 , -8.35296807e+00 ] ,
                [ 1.52727831e+09 , -8.00565670e+00 ] ,
                [ 1.52728016e+09 , -7.71155135e+00 ] ]
        
        self.gui_ROI_a = pg.PolyLineROI( pts , pen=(6 , 9) , closed=True )
        
        self.gui_plot_a.addItem( self.gui_ROI_a )
        
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
    
    def init_gui_plot_b( self ):
        time_axis = pg.DateAxisItem( utcOffset=0 )
        
        pb = self.gui_glw_b.addPlot(
                title="J" ,
                axisItems={ 'bottom': time_axis } )
        
        self.gui_plot_b = pb
    
    def init_gui_buttons( self ):
        l1 = [ self.gui_but_fit_mmd_mconc ,
               self.gui_but_fit_mmd_appea ,
               self.gui_but_fit_mmd_mmode , ]
        
        l2 = [ self.gui_but_plot_mmd_mconc ,
               self.gui_but_plot_mmd_appea ,
               self.gui_but_plot_mmd_mmode ,
               ]
        
        l3 = [
                self.gui_but_save_mmd_mconc,
                self.gui_but_save_mmd_appea,
                self.gui_but_save_mmd_mmode,
                ]
        
        l4 = [
                self.gui_but_save_roi,
                ]
        
        for l in l1:
            self.gui__lw_d.addWidget( l )
        
        self.gui__lw_d.nextRow()
        
        for l in l2:
            self.gui__lw_d.addWidget( l )

        self.gui__lw_d.nextRow()

        for l in l3:
            self.gui__lw_d.addWidget( l )

        self.gui__lw_d.nextRow()

        for l in l4:
            self.gui__lw_d.addWidget( l )
            
        self.gui_but_fit_mmd_appea.clicked.connect(self.gui_but_fit_mmd_appea_clicked)
        
        self.gui_but_plot_mmd_appea.clicked.connect(self.gui_but_plot_mmd_appea_clicked)

        self.gui_but_save_mmd_appea.clicked.connect(self.gui_but_save_mmd_appea_clicked )
        
        self.gui_but_save_roi.clicked.connect(self.gui_but_save_roi_clicked)
        
    
    def init_gui_spins( self ):
        s1 = pg.SpinBox( value=3.e-9 , int=False , dec=True , minStep=1.e-10 ,
                         step=1.e-10 , decimals=5 , suffix='m' , siPrefix=True )
        s2 = pg.SpinBox( value=6.e-9 , int=False , dec=True , minStep=1.e-10 ,
                         step=1.e-10 , decimals=5 , suffix='m' , siPrefix=True )
        s3 = pg.SpinBox( value=1.500 , int=False , dec=True , minStep=1.e-10 ,
                         step=0.1 , decimals=5 )
        s4 = pg.SpinBox( value=0.500 , int=False , dec=True , minStep=1.e-10 ,
                         step=0.1 , decimals=5 )
    
        t1 = 'min Dp'
        t2 = 'max Dp'
        t3 = 'smooth x'
        t4 = 'smooth y'
    
        self.gui_spin_dp_mn = s1
        self.gui_spin_dp_mx = s2
        self.gui_spin_smooth_x = s3
        self.gui_spin_smooth_y = s4
    
        self.gui_spin_dp_mn.sigValueChanged.connect(
                self.replot_smooth_ip_data )
        self.gui_spin_dp_mx.sigValueChanged.connect(
                self.replot_smooth_ip_data )
        self.gui_spin_smooth_x.sigValueChanged.connect(
                self.replot_smooth_ip_data )
        self.gui_spin_smooth_y.sigValueChanged.connect(
                self.replot_smooth_ip_data )
    
        ss = [ self.gui_spin_dp_mn ,
               self.gui_spin_dp_mx ,
               self.gui_spin_smooth_x ,
               self.gui_spin_smooth_y , ]
    
        tt = [ t1 , t2 , t3 , t4 ]
    
        self.gui__lw_d.nextRow()
        for s , t in zip( ss , tt ):
            ly = self.gui__lw_d.addLayout()
            ly.setMaximumHeight( 80 )
            ly.addLabel( t )
            ly.nextRow()
            ly.addWidget( s )

    def init_gui_console_e( self ):
        namespace = { 'pg': pg , 'np': np , 'app': self }
        text = ''
        self.gui_console = pyqtgraph_back.console.ConsoleWidget(
                namespace=namespace , text=text )
        self.gui__lw_e.addWidget( self.gui_console )

    def gui_but_save_roi_clicked(self):
        self.save_roi()
    
    def gui_but_fit_mmd_appea_clicked( self ):
        sa = self.get_smooth_ip_data()
        ra = self.ip_darray
        # noinspection PyTypeChecker
        pts = get_roi_pol_coords( self.gui_ROI_a )
        sd = self.project_path_appearance
        amf = Amf.AppearanceModeFit( ra , sa , pts , sd )
        self.fits_AMF = amf
        self.gui_plot_a.removeItem(self.appea_curve)
        self.plot_appea_lin()
        
    def gui_but_save_mmd_appea_clicked( self ):
        ip_mode = self.ip_mode
        sign = self.ip_sign
        self.fits_AMF.save_fit_df( ip_mode , sign )
    
    def gui_but_plot_mmd_appea_clicked( self ):
        color = self.appea_color
        dff = self.fits_AMF.df
        g_lay_3 = self.gui_glw_c
        par = self.ip_darray
        parG = self.get_smooth_ip_data()
        pls    = self.gui_plot_c_list
        fun = self.fits_AMF.fit_function
        pars = self.fits_AMF.par_order

        # noinspection PyTypeChecker
        plot_multicurves(
                color=color ,
                dff=dff ,
                g_lay_3=g_lay_3 ,
                par=par ,
                parG=parG ,
                pls=pls ,
                fun=fun ,
                pars=pars ,
                )


    
    def launch_qapp( self ):
        from IPython import get_ipython
        _ipython = get_ipython()
        # if interactiva ipython
        if _ipython is not None:
            _magic = _ipython.magic
            # _magic( 'load_ext autoreload' )
            # _magic( 'autoreload 2' )
            _magic( 'gui qt5' )
            # noinspection PyStatementEffect
            self.gui_qapp
        # if not interactive
        else:
            self.gui_qapp.exec_()
    
    def set_ip_mode( self , ip_mode , ip_sign):
        assert ip_mode in ['ion', 'particle']
        assert ip_sign in ['pos', 'neg' , 'neu']
        self.ip_mode = ip_mode
        self.ip_sign = ip_sign
    
    def set_ip_data_array( self , da ):
        self.ip_darray = da
    
    def set_project_path( self , path_root ):
        self.project_path_root = path_root
        assert os.path.isdir( path_root )
        
        self.project_path_roi = os.path.join( path_root ,
                                              'regions_of_interest' )
        os.makedirs( self.project_path_roi , exist_ok=True )
        
        self.project_path_appearance = os.path.join( path_root ,
                                                     'appearance_fit' )
        os.makedirs( self.project_path_appearance , exist_ok=True )
    
    def set_gui_open_combo_box( self , pattern):
        import glob
        files = glob.glob(pattern)
        self.gui_combo_open.addItems(files)
        self.gui__lw_d.nextRow()
        self.gui__lw_d.addWidget(self.gui_combo_open, colspan=4)
    
    def plot_ip_size_dist( self , autoLevels=True ):
        da0 = self.ip_darray
        
        set_image_data(
                da0 ,
                self.gui_img_a ,
                autoLevels=autoLevels
                )
    
    def get_smooth_ip_data( self ):
        x = self.gui_spin_smooth_x.value()
        x = float( x )
        
        y = self.gui_spin_smooth_y.value()
        y = float( y )
        
        da = self.ip_darray
        
        sda = fu.filter(da, x, y)
        
        return sda
    
    def replot_smooth_ip_data( self ):
        sda = self.get_smooth_ip_data()
        img = self.gui_img_a
        set_image_data( sda , img , autoLevels=False )
    
    def save_roi( self ):
        roi_name = get_roi_name( self.gui_ROI_a , self.ip_mode, self.ip_sign)
        roi_path = get_roi_path( self.project_path_roi , roi_name )
        roi_df = get_roi_df( self.gui_ROI_a )
        roi_df_save( roi_df , roi_path )
    
    def load_roi_csv( self , csv_name ):
        path = get_roi_path( self.project_path_roi , csv_name )
        df = pd.read_csv( path )
        roi = self.gui_ROI_a
        roi.setPos( [ 0 , 0 ] )
        roi.setPoints( df[ [ 'time_secs' , 'lDp_m' ] ].values )

    def plot_appea_lin( self ):
        dff = self.fits_AMF.df
        color = self.appea_color
        x = dff[ 'x0' ].values.astype( float )
        ly = dff.reset_index()[ 'lDp' ].values.astype( float )
        y = 10 ** ly
    
        curve = self.gui_plot_a.plot( x , y ,
                              pen=color ,
                              symbolBrush=color ,
                              symbolPen='w' ,
                              symbol='x' ,
                              symbolSize=2 ,
                              name="appearance" )
        self.appea_curve = curve
        # return curve


def set_image_data( da , img , autoLevels ):
    d0 , d1 , t00 , t11 = get_darray_bounds( da )
    da = da.where( da > 1 , 1 )
    lda = np.log10( da )
    # lda = lda.where(lda>0,0)
    data = lda.values
    img.setImage( data , autoLevels=autoLevels )
    width = t11 - t00
    height = d1 - d0
    # noinspection PyUnresolvedReferences
    rect = QtCore.QRectF( t00 , d0 , width , height )
    img.setRect( rect )


def get_darray_bounds( da: xr.DataArray ):
    """get the bounds for the darray"""
    assert 'time' in list( da.coords )
    assert 'lDp' in list( da.coords )
    
    t0 , t1 = fu.infer_interval_breaks( da[ 'time' ] )[ [ 0 , -1 ] ]
    d0 , d1 = fu.infer_interval_breaks( da[ 'lDp' ] )[ [ 0 , -1 ] ]
    t00 = (t0 - np.datetime64( '1970' )) / np.timedelta64( 1 , 's' )
    t11 = (t1 - np.datetime64( '1970' )) / np.timedelta64( 1 , 's' )
    return d0 , d1 , t00 , t11


def get_roi_pol_coords( roi ):
    """gets the ROI list of coords in the axis mapping"""
    pts = roi.getState()[ 'points' ]
    pts = [ roi.mapToParent( p ) for p in pts ]
    xy_list = np.array( [ [ p.x() , p.y() ] for p in pts ] )
    return xy_list


def get_roi_name( gui_ROI_a, particle_or_ion:str, sign:str ):
    roi = gui_ROI_a
    arr = get_roi_pol_coords( roi )
    secs = arr[ : , 0 ]
    mean_secs = secs.mean()
    dt = pd.to_datetime( mean_secs , unit='s' )
    dt = dt.strftime( '%Y-%m-%dT%H.csv' )
    name = f'roi_{particle_or_ion}_{sign}_{dt}'
    return name


def get_roi_df( gui_ROI_a ):
    roi = gui_ROI_a
    arr = get_roi_pol_coords( roi )
    return pd.DataFrame( arr , columns=[ 'time_secs' , 'lDp_m' ] )


def roi_df_save( roi_df: pd.DataFrame , roi_path ):
    roi_df.to_csv( roi_path , index=False )


def get_roi_path( project_path_roi , roi_name ):
    return os.path.join( project_path_roi , roi_name )


def plot_multicurves( color     ,
                      dff       ,
                      g_lay_3   ,
                      par       ,
                      parG      ,
                      pls       ,
                      fun       ,
                      pars
                      ):
    min_height = 100
    while pls:
        g_lay_3.removeItem( pls.pop( 0 ) )
    ll = len( dff )
    for ii in range( ll ):
        row = dff.reset_index().iloc[ ii ]
        
        lDp = row[ 'lDp' ]
        
        #     plt.plot(x,y)
        #     plt.plot(x,10**AA.gauss_fun(x,row['a'],row['sigma'],
        #     row['x0'],row['D']))
        
        pl = g_lay_3.addPlot( row=ll - ii , col=0 , axisItems={
                'bottom': pg.DateAxisItem() } )
        pl.setMinimumHeight(50)
        pls.append( pl )
        
        pp = parG.loc[ { 'lDp': lDp } ]
        x = pp[ 'secs' ].values
        y = pp.values
        pl.plot( x , y )
        
        pp = par.loc[ { 'lDp': lDp } ]
        x = pp[ 'secs' ].values
        y = pp.values
        pl.plot( x , y , pen=(200 , 0 , 0) )
        row_pars = [ row[ p ] for p in pars ]
        pl.plot( x ,
                 fun( x , *row_pars ) ,
                 pen=color
                 )
        pl.enableAutoRange( 'y' , 0.99 )
        #     pl.showGrid(x = True, y = True, alpha = 1.0)
        pl.getAxis( 'left' ).setWidth( 80 )
        pl.setLabel( 'left' , f'{(10 ** lDp) * 1e9:4.1f}nm' )

        isoLine = pg.InfiniteLine([row['x0'],0], angle=90 , movable=False , pen='g' )
        pl.addItem( isoLine )
        
        if ii > 0:
            pl.setXLink( pls[ 0 ] )
            #         pl.setYLink(pls[0])
            pl.hideAxis( 'bottom' )
        else:
            pass
    
    g_lay_3.setMinimumHeight(min_height * ll)
