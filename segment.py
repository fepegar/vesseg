from pathlib import Path

import click

from vesseg.pipeline import SegmentPipeline


@click.command()
@click.option('--prob', is_flag=True, default=False,
              help='Output foreground probability instead of binary image')
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path, output_path, prob):
    """Segment brain vessels in DSA image"""
    repo_dir = Path(__file__).parent
    segment = SegmentPipeline(input_path, output_path,
                              repo_dir, output_probability=prob)
    segment.run()
