'''
add accesors to xarray so that conversions are easier
'''
import xarray as xr
import numpy as np
from xarray.plot.plot import _infer_interval_breaks as infer_interval_breaks
import matplotlib as mpl
import matplotlib.colors

# @xr.register_dataset_accessor("geo")
# class GeoAccessor:
#     def __init__(self, xarray_obj):
#         self._obj = xarray_obj
#         self._center = None
#
#     @property
#     def center(self):
#         """Return the geographic center point of this dataset."""
#         if self._center is None:
#             # we can use a cache on our accessor objects, because accessors
#             # themselves are cached on instances that access them.
#             lon = self._obj.latitude
#             lat = self._obj.longitude
#             self._center = (float(lon.mean()), float(lat.mean()))
#         return self._center
#
#     def plot(self):
#         """Plot data on a map."""
#         return "plotting!"


@xr.register_dataset_accessor("bnn")
@xr.register_dataarray_accessor("bnn")
class ToSec:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
    #         self._center = None

    #     @property
    def from_time2sec(self,col='time'):
        """change time to sec"""
        date = self._obj[col]
        s1 = date - np.datetime64(0, 'Y')
        s2 = s1 / np.timedelta64(1, 's')
        return self._obj.assign_coords({'secs':s2})
    def from_sec2time(self,col='secs'):
        o =self._obj
        secs = o[col].astype('datetime64[s]')
        return o.assign_coords({'time':secs})

    def from_Dp2lDp(self,col='Dp'):
        o =self._obj
        lDp =  np.log10(o[col])
        return o.assign_coords({'lDp':lDp})

    def from_lDp2Dp(self):
        o =self._obj
        Dp =  10**(o['lDp'])
        return o.assign_coords({'Dp':Dp})

    def from_lDp2dlDp(self):
        o =self._obj
        lDp =  o['lDp']
        borders  = infer_interval_breaks(lDp)
        d = borders[1:] - borders[:-1]
        d1 = lDp*0 + d
        return o.assign_coords({'dlDp':d1})

    def from_Dp2dDp(self):
        o =self._obj
        Dp =  o['Dp']
        borders  = infer_interval_breaks(Dp)
        d = borders[1:] - borders[:-1]
        d1 = Dp*0 + d
        return o.assign_coords({'dDp':d1})


    def set_time(self):
        # o = self._obj
        o1 = self.from_sec2time()
        o2 = o1.swap_dims( { 'secs':'time'})
        return o2

    def set_Dp(self):
        o1 = self._obj
        # o1 = self.from_sec2time()
        o2 = o1.swap_dims( { 'lDp':'Dp'})
        return o2

    def set_lDp(self):
        o1 = self._obj
        # o1 = self.from_sec2time()
        o2 = o1.swap_dims( { 'Dp':'lDp'})
        return o2

    def set_sec(self):
        # o = self._obj
        o1 = self.from_time2sec()
        o2 = o1.swap_dims( { 'time':'secs'})
        return o2

    def set_Dp(self):
        # o = self._obj
        o1 = self.from_lDp2Dp()
        o2 = o1.swap_dims( { 'lDp':'Dp'})
        return o2

    def plot(self, *args, **kwargs):

        self.set_time()
        o = self._obj
        q1 = o.quantile(.05)
        q2 = o.quantile(.95)
        o.plot(x='time',norm=mpl.colors.LogNorm(vmin=q1,vmax=q2), cmap='cividis',
               *args, **kwargs
               )
    def get_dN(self, d1, d2):
        self._obj = self.from_lDp2dlDp()
        o = self.set_Dp()
        o1 = o.loc[{'Dp':slice(d1,d2)}]
        dmin = o1['Dp'].min().item()
        dmax = o1['Dp'].max().item()

        dN = (o1 * o1['dlDp'])

        return dN, dmin, dmax


