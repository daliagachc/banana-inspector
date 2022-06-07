from skimage import measure
import numpy as np
import pandas as pd
import matplotlib as mpl

def get_gr_low(dd1,qq,d1,d2,roi):
    df = get_contour(dd1, qq)

    df1 = is_inside_roi(df, roi)

    # df1.plot.scatter(x='x',y='y')

    df3 = take_first_x(df1)

    # df3.plot.scatter(x='x',y='y')

    df4 = below_and_above(d1, d2, df3)
    # df4.plot.scatter(x='x',y='y')
    return df4

def below_and_above(d1, d2, df3):
    return df3[((df3['y'] >= d1) & (df3['y'] < d2))]

def take_first_x(df1):
    df2 = df1.sort_values('x')
    bo = df2.duplicated('y', keep='first')
    df3 = df2[~bo]
    return df3

def is_inside_roi(df, roi):
    path = mpl.path.Path(roi, closed=True)
    inside2 = path.contains_points(df)
    df1 = df[inside2]
    return df1

def get_contour(dd1, qq):
    contours = measure.find_contours(dd1.values, qq)
    # plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    dsec = dd1['secs'].swap_dims({'secs': 'summy'})
    ddp = dd1['lDp'].swap_dims({'lDp': 'dummy'})
    crs = np.concatenate(contours)
    x = dsec['secs'].interp({'summy': crs[:, 1]}, 'linear').values
    y = ddp['lDp'].interp({'dummy': crs[:, 0]}, 'nearest').values
    df = pd.DataFrame(np.array([x, y]).T, columns=['x', 'y'])
    return df

def gam_fit(dfc):
    from pygam import LinearGAM
    # X = np.log10((dfc[['x']].values - dfc['x'].min() )/3600 + .5)

    X = dfc[['x']].values


    # y = dfc['Dp'].values
    y = dfc['y'].values

    lX = len(X)-1

    # %%

    from pygam.datasets import mcycle

    # X, y = mcycle(return_X_y=True)

    gam = LinearGAM(n_splines=lX).gridsearch(X, y)
    y = gam.predict(X)

    return y

def gam_fit(dfc):
    from pygam import LinearGAM
    # X = np.log10((dfc[['x']].values - dfc['x'].min() )/3600 + .5)


    X = dfc[['x']].values
    print(X)


    # y = dfc['Dp'].values
    y = dfc['y'].values

    lX = len(X)-1

    # %%

    from pygam.datasets import mcycle

    # X, y = mcycle(return_X_y=True)

    gam = LinearGAM(n_splines=lX).gridsearch(X, y)
    y = gam.predict(X)

    return y

def get_gr(dd1,dd2,qq,qq2,d1,d2,d3,roi):

    df1 = get_gr_low(dd1,qq,d1,d2,roi)
    df2 = is_inside_roi(get_contour(dd2, qq2),roi)

    df3 = take_first_x(df2)

    df4 = below_and_above(d2,d3,df3)
    dfc = pd.concat([df1,df4])
    dfc['Dp']=10**(dfc['y'])
    dfc['y_fit']=gam_fit(dfc)
    return dfc