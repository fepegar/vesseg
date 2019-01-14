import SimpleITK as sitk


def keep_largest_component(input_path, output_path=None):
    if output_path is None:
        output_path = input_path
    image = sitk.ReadImage(str(input_path))
    labels = sitk.ConnectedComponent(image)
    relabeled = sitk.RelabelComponent(labels)
    largest = relabeled == 1
    sitk.WriteImage(largest, str(output_path))


def touches_border(image_path):
    image = sitk.ReadImage(str(image_path))
    array = sitk.GetArrayViewFromImage(image)
    touches = (array[0, ...].any()
               or array[-1, ...].any()
               or array[:, 0, :].any()
               or array[:, -1, :].any()
               or array[..., 0].any()
               or array[..., -1].any()
              )
    return touches


def pad(input_path, output_path, lower=(1, 1, 1), upper=(1, 1, 1), value=0):
    image = sitk.ReadImage(str(input_path))
    padded = sitk.ConstantPad(image, lower, upper, value)
    sitk.WriteImage(padded, str(output_path))
