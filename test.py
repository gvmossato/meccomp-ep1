import numpy as np

def test_h(h,contours_pos,grid_limits):
    mash_grid = np.linspace(grid_limits[0],grid_limits[1]+h,h)

    return np.all([e in mash_grid for e in np.array(contours_pos)])