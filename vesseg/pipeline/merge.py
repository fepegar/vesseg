from pathlib import Path
from tqdm import tqdm
import SimpleITK as sitk
from ..processing.image import resample_isotropic, resample, merge_segmentations

DEFAULT_SPACING = 0.5  # mm


class MergePipeline:
    def __init__(self,
                 reference_path,
                 images_and_transforms,
                 output_path,
                 spacing=DEFAULT_SPACING):
        self.reference_path = Path(reference_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.images_and_transforms = images_and_transforms
        self.spacing = spacing


    def run(self):
        resampled_reference = resample_isotropic(
            self.reference_path, self.spacing)
        resampled_images = [
            resample(resampled_reference, floating_path, transform_path)
            for floating_path, transform_path
            in tqdm(self.images_and_transforms)
        ]
        print('Transforming images...')
        merge_segmentations(resampled_images, self.output_path)
