import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap
from shapely.affinity import scale

# ---------------------------------------------------
# Load and extract relevant geographical data

shapefile_path = './distritos-shapefile/distritos.shp'
gdf_distritos = gpd.read_file(shapefile_path)

shapefile_path = './concelhos-shapefile/concelhos.shp'
gdf_concelhos = gpd.read_file(shapefile_path)

shapefile_path = './geo_data/Cont_AAD_CAOP2017.shp'
gdf = gpd.read_file(shapefile_path)

min_x = min(gdf.bounds['minx'])
min_y = min(gdf.bounds['miny'])
gdf['geometry'] = gdf['geometry'].translate(xoff=-min_x, yoff=-min_y)

gdf_concelhos = gdf_concelhos.to_crs(gdf.crs)
gdf_concelhos = gdf_concelhos[gdf_concelhos.geometry.centroid.x >= -0.5e6]
min_x = min(gdf_concelhos.bounds['minx'])
min_y = min(gdf_concelhos.bounds['miny'])
gdf_concelhos['geometry'] = gdf_concelhos['geometry'].translate(xoff=- min_x - 2300 - 160, yoff=- min_y - 60)

gdf_distritos = gdf_distritos.to_crs(gdf.crs)
gdf_distritos = gdf_distritos[gdf_distritos.geometry.centroid.x >= -0.5e6]
min_x = min(gdf_distritos.bounds['minx'])
min_y = min(gdf_distritos.bounds['miny'])
gdf_distritos['geometry'] = gdf_distritos['geometry'].translate(xoff=- min_x - 2500 + 20, yoff=- min_y - 70)

longitudes = np.loadtxt("parishes_coordinates.dat")[:, 0]
latitudes = np.loadtxt("parishes_coordinates.dat")[:, 1]

# ---------------------------------------------------
# Plot the data using Matplotlib

# Normalize the values to the range [0, 1]
norm = Normalize(vmin=-20, vmax=50)
#norm = Normalize(vmin=-10, vmax=25)

values = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
colors = [
    (1.0, 0.0, 1.0),  # Magenta
    (0.7, 0.0, 1.0),  # Purple
    (0.5, 0.0, 1.0),  # Violet
    (0.0, 0.0, 1.0),  # Blue
    (0.0, 0.2, 1.0),  # Royal Blue
    (0.0, 0.7, 1.0),  # Deep Sky Blue
    (0.0, 1.0, 1.0),  # Cyan
    (0.0, 0.8, 0.8),  # Turquoise
    (0.0, 1.0, 0.0),  # Light Green
    (0.5, 1.0, 0.0),  # Yellow Green
    (1.0, 1.0, 0.0),  # Yellow
    (1.0, 0.5, 0.0),  # Orange
    (1.0, 0.0, 0.0),   # Red
    (0.5, 0.0, 0.0),   # Red
    (0.0, 0.0, 0.0),   # Red
]

custom_cmap = LinearSegmentedColormap.from_list('cold_hot', colors, N=1024)

# Create the colormap
#cmap = plt.cm.get_cmap('gist_rainbow_r')
cmap=custom_cmap

# Create a ScalarMappable to map values to colors
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

fig, ax = plt.subplots()

temperatures = np.loadtxt("./temperatures/temperatures_2023_12_20_14")
#ax2 = gdf_concelhos.plot(ax=ax, edgecolor='black')
ax  = gdf.plot(ax=ax, color=cmap(norm(temperatures)), edgecolor='none')
ax2 = gdf_concelhos.plot(ax=ax, alpha=0.7, facecolor='none', edgecolor='black', linewidth=0.1)
ax3 = gdf_distritos.plot(ax=ax, alpha=0.7, facecolor='none', edgecolor='black', linewidth=0.3)

cbar = fig.colorbar(sm, ax=ax)
ax.set_title('2023_12_20_' + str(14))


def update_colors(gdf, colors):
    for polygon, color in zip(ax.patches, colors):
        polygon.set_facecolor(color)


while True:
    for i in range (0, 73):
        # Update the colormap
        temperatures = np.loadtxt("./temperatures/temperatures_2023_12_" + str((20 + (i + 14)//24)) + '_' + str((i + 14)%24))
        ax.collections[0].set_facecolor(cmap(norm(temperatures)))
        
        ax.set_title("2023-12-" + str(20 + (i + 14)//24) + ' ' + str((i + 14)%24) + "h")
        
        # Redraw the updated plot
        fig.canvas.draw()

        # Pause for a short time (optional)
        plt.pause(0.25)

plt.show()