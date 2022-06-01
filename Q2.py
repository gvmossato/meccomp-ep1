import numpy as np

from EPLib import Plate

# func_boundaries = {
#     [(0.03, 0.03), np.deg2rad((00.0, 40.0))] : func_1(),
#     [(0.05, 0.05), np.deg2rad((00.0, 18.0))] : func_2(),
#     [(0.08, 0.08), np.deg2rad((00.0, 40.0))] : func_2(),
#     [(0.03, 0.11), np.deg2rad((40.0, 40.0))] : func_2(),
#     [(0.05, 0.08), np.deg2rad((18.0, 18.0))] : func_2(),
# }

r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

func_boundaries = {}

plate = Plate(r_range, phi_range, func_boundaries)

print(f'meshgrid finalizada! {plate.meshgrid.shape}')

plate.plot('meshgrid')
