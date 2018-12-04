import SimpleITK as sitk


def remove_small_components(input_path, output_path=None):
    if output_path is None:
        output_path = input_path
    image = sitk.ReadImage(str(input_path))
    labels = sitk.ConnectedComponent(image)
    relabeled = sitk.RelabelComponent(labels)
    largest = relabeled == 1
    sitk.WriteImage(largest, str(output_path))
