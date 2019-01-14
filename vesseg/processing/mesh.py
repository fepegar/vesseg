import vtk
from .image import touches_border, pad


def read_image(image_path):
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(str(image_path))
    reader.Update()
    image = reader.GetOutput()
    qform = reader.GetQFormMatrix()
    return image, qform


def marching_cubes(image_path, compute_normals=True, value=0.5):
    if touches_border(image_path):
        import tempfile
        tempdir = Path(tempfile.gettempdir())
        temp_path = tempdir / 'padded.nii.gz'
        pad(image_path, temp_path)
        image_path = temp_path
    image, qform = read_image(image_path)
    marching_cubes_filter = vtk.vtkMarchingCubes()
    marching_cubes_filter.ComputeScalarsOff()
    marching_cubes_filter.SetComputeNormals(compute_normals)
    marching_cubes_filter.SetValue(0, value)
    marching_cubes_filter.SetInputData(image)
    marching_cubes_filter.Update()
    surface_voxel = marching_cubes_filter.GetOutput()
    surface_world = apply_transform(surface_voxel, qform)
    return surface_world


def apply_transform(poly_data, matrix):
    transform = vtk.vtkTransform()
    transform.SetMatrix(matrix)
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetTransform(transform)
    transform_filter.SetInputData(poly_data)
    transform_filter.Update()
    return transform_filter.GetOutput()


def smooth(poly_data, pass_band):
    """
    Smooth poly data
    Adapted from Csaba Pinter's code:
    https://github.com/Slicer/Slicer/blob/47d1643030d8c6e7cdb2953a8ad5acfee1836803/Libs/vtkSegmentationCore/vtkBinaryLabelmapToClosedSurfaceConversionRule.cxx#L216-L231

    # This formula maps:
    # 0.0  -> 1.0 (almost no smoothing),
    # 0.25 -> 0.01 (average smoothing),
    # 0.5  -> 0.001 (more smoothing),
    # 1.0  -> 0.0001 (very strong smoothing).
    """
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputData(poly_data)
    smoother.SetPassBand(pass_band)
    smoother.BoundarySmoothingOff()
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()
    smoother.Update()
    return smoother.GetOutput()


def add_normals(poly_data):
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly_data)
    normals.ConsistencyOn()
    normals.SplittingOff()
    normals.Update()
    return normals.GetOutput()


def write_surface(surface, surface_path):
    from os.path import splitext
    _, suffix = splitext(str(surface_path))
    if suffix == '.vtk':
        writer = vtk.vtkPolyDataWriter()
    elif suffix == '.ply':
        writer = vtk.vtkPLYWriter()
    elif suffix == '.vtp':
        writer = vtk.vtkXMLPolyDataWriter()
    elif suffix == '.stl':
        writer = vtk.vtkSTLWriter()
    writer.SetFileName(str(surface_path))
    writer.SetInputData(surface)
    writer.Write()
