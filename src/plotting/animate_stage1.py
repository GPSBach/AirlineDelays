import os
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

from mpl_toolkits.basemap import Basemap

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pygrib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import time

def print_time(t0):
    t1 = time.time()
    return t1-t0

stride = 5

# starting and ending viewazimuths
azim_start = 270
azim_end = 270

# starting and ending view elevations
elev_start = 90
elev_end = 90

# starting and ending zooms
dist_start = 300
dist_end = 300

# starting and ending center latitude
lat_start = 43
lat_end = 43

# starting and ending longitude
lon_start = -97
lon_end = -97

# starting and ending layer separation
delev_start = 0
delev_end = 0

# delta center degrees
# latitude window for center
# tradoff with dist
ddeg = 1

#save files setup
savepath = '/home/tbowling/airline/plots/'
filename = 'stage1_'


num_steps = 10

t0 = time.time()

variables = ['Wind speed (gust)']
colors = ['plasma']
ranges = [(0,10)]

for i in range(num_steps):
    delev = delev_start-i*((delev_start-delev_end)/(num_steps-1))
    hour = str(i-24*(i//24)).zfill(2)
    day = str(1+i//24).zfill(2)
    try:
        grbs = pygrib.open(f'/home/tbowling/airline/data/weather/rap_130_201808{day}_{hour}00_000.grb2')
    except:
        pass
    
    datas = []
    elev = np.arange(len(variables))*delev

    for variable in variables:
        grb = grbs.select(name=variable)[0]
        lats, lons = grb.latlons()
        datas.append(grb['values'])

    map = Basemap(llcrnrlon=-360,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=90,)

    fig = plt.figure(figsize=[10,10],dpi=150)
    ax = Axes3D(fig)

    ax.add_collection3d(map.drawcoastlines(linewidth=0.35))
    ax.add_collection3d(map.drawcountries(linewidth=0.35))

    ax.set_axis_off()
    ax.azim = azim_start-i*((azim_start-azim_end)/(num_steps-1))
    ax.elev = elev_start-i*((elev_start-elev_end)/(num_steps-1))
    ax.dist = dist_start-i*((dist_start-dist_end)/(num_steps-1))
    
    center_lat = lat_start-i*((lat_start-lat_end)/(num_steps-1))
    center_lon = lon_start-i*((lon_start-lon_end)/(num_steps-1))


    for ix,data in enumerate(datas):
        # fourth dimention - colormap
        # create colormap according to x-value (can use any 50x50 array)
        color_dimension = data # change to desired fourth dimension
        minn, maxx = color_dimension.min(), color_dimension.max()
        norm = matplotlib.colors.Normalize(minn, maxx)
        m = plt.cm.ScalarMappable(norm=norm, cmap=colors[ix])
        m.set_array([])
        fcolors = m.to_rgba(color_dimension)

        ax.plot_surface(lons,lats,np.ones(lats.shape)*elev[ix]+delev/10,cstride=stride,rstride=stride,facecolors=fcolors, vmin=ranges[ix][0], vmax=ranges[ix][0], shade=False)

    ax.set_xlim3d(center_lon-ddeg,center_lon+ddeg)
    ax.set_ylim3d(center_lat-ddeg,center_lat+ddeg)
    if i < 10:
        fig.savefig(f'{savepath}{filename}0000{i}.png', dpi=fig.dpi)
    elif i >=10 and i < 100:
        fig.savefig(f'{savepath}{filename}000{i}.png', dpi=fig.dpi)
    elif i >=100 and i < 1000:
        fig.savefig(f'{savepath}{filename}00{i}.png', dpi=fig.dpi)
    elif i > 1000:
        fig.savefig(f'{savepath}{filename}0{i}.png', dpi=fig.dpi)
    plt.close()
    print(f'Printed {filename}0000{i}.png in',print_time(t0),'seconds')
    t0 = time.time()