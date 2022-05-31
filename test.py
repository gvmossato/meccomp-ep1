import numpy as np

def test_h(h,contours_pos,mash_grid)

    return np.all([e in mash_grid for e in np.array(contours_pos)])