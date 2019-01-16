import click
from vesseg.pipeline.merge import MergePipeline, DEFAULT_SPACING


@click.command()
@click.option('--spacing', default=DEFAULT_SPACING,
              help='Reference spacing')
@click.argument('reference_path', type=click.Path(exists=True), nargs=1)
@click.argument('output_path', type=click.Path(), nargs=1)
@click.argument('images_and_transforms', type=click.Path(exists=True), nargs=-1)
def main(reference_path, output_path, images_and_transforms, spacing):
    """Merge binary images into a common reference space"""
    images_paths = images_and_transforms[::2]
    transforms_paths = images_and_transforms[1::2]
    images_and_transforms = zip(images_paths, transforms_paths)
    pipeline = MergePipeline(
        reference_path,
        images_and_transforms,
        output_path,
        spacing=spacing,
    )
    pipeline.run()
