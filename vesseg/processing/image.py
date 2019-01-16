import SimpleITK as sitk
import numpy as np
from tqdm import tqdm


def read(input_path):
    return sitk.ReadImage(str(input_path))


def write(image, output_path):
    sitk.WriteImage(image, str(output_path))


def to_uchar(image_path):
    image = read(image_path)
    if image.GetPixelID != sitk.sitkUInt8:
        image = sitk.Cast(image, sitk.sitkUInt8)
        write(image, image_path)


def keep_largest_component(input_path, output_path=None):
    if output_path is None:
        output_path = input_path
    image = read(input_path)
    labels = sitk.ConnectedComponent(image)
    relabeled = sitk.RelabelComponent(labels)
    largest = relabeled == 1
    write(largest, output_path)


def touches_border(image_path):
    image = read(image_path)
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
    image = read(input_path)
    padded = sitk.ConstantPad(image, lower, upper, value)
    write(padded, output_path)


def resample_isotropic(image_path, spacing):
    reference = read(image_path)

    output_spacing = 3 * (spacing,)
    reference_spacing = np.array(reference.GetSpacing())
    referenceSize = np.array(reference.GetSize())

    output_size = reference_spacing / output_spacing * referenceSize
    output_size = np.round(output_size).astype(np.uint32)
    # tuple(output_size) does not work, see
    # https://github.com/Radiomics/pyradiomics/issues/204
    output_size = output_size.tolist()

    resample = sitk.ResampleImageFilter()
    resample.SetInterpolator(sitk.sitkNearestNeighbor)
    resample.SetOutputDirection(reference.GetDirection())
    resample.SetOutputOrigin(reference.GetOrigin())  # should I fix this?
    resample.SetOutputPixelType(reference.GetPixelID())
    resample.SetOutputSpacing(output_spacing)
    resample.SetSize(output_size)
    resampled = resample.Execute(reference)
    return resampled


def merge_segmentations(images, output_path):
    result = images[0]
    for image in tqdm(images[1:]):
        result = sitk.Or(result, image)
    write(result, output_path)


def resample(reference_image, floating_path, transform_path):
    transform = sitk.ReadTransform(str(transform_path))
    floating_image = read(floating_path)
    resampled = sitk.Resample(
        floating_image,
        reference_image,
        transform,
        sitk.sitkNearestNeighbor,
        0,
        floating_image.GetPixelID()
    )
    return resampled


def extract_foreground(image_path):
    return
    # TODO
    # nii = nib.load(image_path)
    # if len(nii.shape) == 3:
    #     return

    # # Extract foreground from 5D image
    # data = nii.get_data()
    # data = data[..., 1].squeeze()
    # nii = nib.Nifti1Image(data, nii.affine)
    # result_path = image_path.replace('.nii.gz', '_foreground.nii.gz')
    # nib.save(nii, result_path)

    # # Threshold probabilities at 0.5
    # label = (data > 0.5).astype(np.uint8)
    # nii = nib.Nifti1Image(label, nii.affine)
    # label_path = image_path.replace('.nii.gz', '_label.nii.gz')
    # nib.save(nii, label_path)
