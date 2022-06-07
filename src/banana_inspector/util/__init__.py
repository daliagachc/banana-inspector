import numpy as np
# import bnn_array
# import coag_sink
# import true_eq
import pandas as pd


def to_sec(date):
    s1 = date - np.datetime64(0, 'Y')
    s2 = s1 / np.timedelta64(1, 's')

    return s2


def str2sec(time):
    sec = to_sec(pd.to_datetime(time))
    return sec