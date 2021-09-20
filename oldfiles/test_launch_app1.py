# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: b37
#     language: python
#     name: b37
# ---

# %%
"""
6/16/21

diego.aliaga at helsinki dot fi
"""

# %% [markdown]
# interactive import

# %%
from IPython import get_ipython
_ipython = get_ipython()
if _ipython is not None:
    _magic = _ipython.magic
    _magic( 'load_ext autoreload' )
    _magic( 'autoreload 2' )

# %%
from npf_analyzer3 import *
import npf_analyzer3 as np3
import os
import xarray as xr
import AppearanceModeFit as Amf

# %%

# %%
try:
    here_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    here_path = os.path.dirname(os.path.abspath(np3.__file__))

# %%
def open_darray( pp ):
    p = os.path.join( here_path , pp )
    ip_darray = np3.fu.open_sum(p)
    
    ip_darray = np3.fu.get_treated_da(ip_darray)
    
    
    da = np3.fu.set_secs_dim(ip_darray)
    da['tempK'] = xr.zeros_like(da['secs']) + 273
    da['presP'] = xr.zeros_like(da['secs']) + 532000
    
    return da

# %%
p1 = 'example_data/lev2_NAISp20180525np.sum'
da1 = open_darray(p1)

# %%
p2 = 'example_data/lev2_NAISp20180527np.sum'
da2 = open_darray(p2)

# %%
root_path = '/tmp/npf'
os.makedirs(root_path, exist_ok=True)

# %%

# %%
self = np3.GuiNpf()
self.set_ip_mode('particle')
self.set_ip_data_array( da1 )

# %%
self.plot_ip_size_dist()
self.set_project_path(root_path)

# %%
sa = self.get_smooth_ip_data()
pts = np3.get_roi_pol_coords(self.gui_ROI_a)
sd = self.project_path_appearance
amf = Amf.AppearanceModeFit(sa,pts,sd)

# %%
import matplotlib.pyplot as plt
f,ax = plt.subplots()
df = amf.df
df['Dp'] = 10**df.index * 1e9
df.plot(x='x0',y='Dp', ax =ax )
df.plot(x='x0_',y='Dp',lw=0,marker='o', ax =ax )

# %%
df.index()

# %%
sa.plot()

# %%
