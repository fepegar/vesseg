import click
from vesseg.pipeline.mesh import MeshPipeline, DEFAULT_SMOOTHING_FACTOR


@click.command()
@click.option('--smoothing-factor', default=DEFAULT_SMOOTHING_FACTOR,
              help='Smoothing factor')
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path, output_path, smoothing_factor):
    """Convert image to mesh"""
    pipeline = MeshPipeline(
        input_path,
        output_path,
        smoothing_factor=smoothing_factor
    )
    pipeline.run()
