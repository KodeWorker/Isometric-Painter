import numpy as np

def InitMesh(grid_min, grid_max, init_pixel=(0, 0, 0, 0)):
    mesh = {0:{}, 1:{}} # Canvas mode: 0/1 (in/out)

    x_grid = grid_max['x'] - grid_min['x']
    y_grid = grid_max['y'] - grid_min['y']
    z_grid = grid_max['z'] - grid_min['z']

    for mode in mesh.keys():
        face_xy = np.empty([x_grid, y_grid], dtype=tuple)
        face_xy.fill(init_pixel)
        mesh[mode]['xy'] = face_xy

        face_yz = np.empty([y_grid, z_grid], dtype=tuple)
        face_yz.fill(init_pixel)
        mesh[mode]['yz'] = face_yz

        face_xz = np.empty([x_grid, z_grid], dtype=tuple)
        face_xz.fill(init_pixel)
        mesh[mode]['xz'] = face_xz

    return mesh
