from pathlib import Path
from ..processing.mesh import marching_cubes, smooth, write_surface

DEFAULT_SMOOTHING_FACTOR = 0


class MeshPipeline:
    def __init__(self,
                 image_path,
                 mesh_path,
                 smoothing_factor=DEFAULT_SMOOTHING_FACTOR):
        self.image_path = Path(image_path).resolve()
        self.mesh_path = Path(mesh_path).resolve()
        self.smoothing_factor = smoothing_factor


    def run(self):
        print('Running marching cubes...')
        poly_data = marching_cubes(self.image_path)
        if self.smoothing_factor > 0:
            print('Smoothing surface...')
            poly_data = smooth(poly_data, self.smoothing_factor)
        print('Writing surface...')
        write_surface(poly_data, self.mesh_path)
        print('Surface written to {self.mesh_path}')
