from pathlib import Path

import click

from vesseg import PostProcessingPipeline


@click.command()
@click.option('--largest-only', is_flag=True, default=False,
              help='Keep only largest connected component')
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path, output_path, largest_only):
    """Morphological postprocessing"""
    pipeline = PostProcessingPipeline(
        input_path,
        output_path,
        largest_only=largest_only
    )
    pipeline.run()
