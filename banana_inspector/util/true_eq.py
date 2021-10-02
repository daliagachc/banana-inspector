# -*- coding: utf-8 -*-
"""
the true eq function (adpatped for xarray)
"""

from __future__ import division


import sys
import warnings
import math

import numpy as np

from pyqtgraph.metaarray import MetaArray
from collections import OrderedDict

# in order of appearance in this file.
# add new functions to this list only if they are to reside in pg namespace.


def eq(a, b):
    """The not so great missing equivalence function: Guaranteed evaluation to a single bool value.
    
    This function has some important differences from the == operator:
    
    1. Returns True if a IS b, even if a==b still evaluates to False.
    2. While a is b will catch the case with np.nan values, special handling is done for distinct
       float('nan') instances using math.isnan.
    3. Tests for equivalence using ==, but silently ignores some common exceptions that can occur
       (AtrtibuteError, ValueError).
    4. When comparing arrays, returns False if the array shapes are not the same.
    5. When comparing arrays of the same shape, returns True only if all elements are equal (whereas
       the == operator would return a boolean array).
    6. Collections (dict, list, etc.) must have the same type to be considered equal. One
       consequence is that comparing a dict to an OrderedDict will always return False.
    """
    if a is b:
        return True

    # The above catches np.nan, but not float('nan')
    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return True

    # Avoid comparing large arrays against scalars; this is expensive and we know it should return False.
    aIsArr = isinstance(a, (np.ndarray, MetaArray))
    bIsArr = isinstance(b, (np.ndarray, MetaArray))
    if (aIsArr or bIsArr) and type(a) != type(b):
        return False

    # If both inputs are arrays, we can speeed up comparison if shapes / dtypes don't match
    # NOTE: arrays of dissimilar type should be considered unequal even if they are numerically
    # equal because they may behave differently when computed on.
    if aIsArr and bIsArr and (a.shape != b.shape or a.dtype != b.dtype):
        return False

    # todo: check that this is doing what we expect
    # we add this so that xarray types are supported
    import xarray
    isda = isinstance(a,xarray.core.dataarray.DataArray)
    isds = isinstance(a,xarray.core.dataset.Dataset)

    isdab = isinstance(b,xarray.core.dataarray.DataArray)
    isdsb = isinstance(b,xarray.core.dataset.Dataset)
    
    if isda or isds :
        return a.identical(b)
    if isdab or isdsb:
        return b.identical(a)

    # Recursively handle common containers
    if isinstance(a, dict) and isinstance(b, dict):
        if type(a) != type(b) or len(a) != len(b):
            return False
        if set(a.keys()) != set(b.keys()):
            return False
        for k, v in a.items():
            if not eq(v, b[k]):
                return False
        if isinstance(a, OrderedDict) or sys.version_info >= (3, 7):
            for a_item, b_item in zip(a.items(), b.items()):
                if not eq(a_item, b_item):
                    return False
        return True
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if type(a) != type(b) or len(a) != len(b):
            return False
        for v1,v2 in zip(a, b):
            if not eq(v1, v2):
                return False
        return True

    # Test for equivalence. 
    # If the test raises a recognized exception, then return Falase
    try:
        try:
            # Sometimes running catch_warnings(module=np) generates AttributeError ???
            catcher =  warnings.catch_warnings(module=np)  # ignore numpy futurewarning (numpy v. 1.10)
            catcher.__enter__()
        except Exception:
            catcher = None
        e = a==b
    except (ValueError, AttributeError): 
        return False
    except:
        print('failed to evaluate equivalence for:')
        print("  a:", str(type(a)), str(a))
        print("  b:", str(type(b)), str(b))
        raise
    finally:
        if catcher is not None:
            catcher.__exit__(None, None, None)
    
    t = type(e)
    if t is bool:
        return e
    elif t is np.bool_:
        return bool(e)
    elif isinstance(e, np.ndarray) or (hasattr(e, 'implements') and e.implements('MetaArray')):
        try:   ## disaster: if a is an empty array and b is not, then e.all() is True
            if a.shape != b.shape:
                return False
        except:
            return False
        if (hasattr(e, 'implements') and e.implements('MetaArray')):
            return e.asarray().all()
        else:
            return e.all()
    else:
        raise TypeError("== operator returned type %s" % str(type(e)))


