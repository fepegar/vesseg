from pathlib import Path

import click

from vesseg import SegmentPipeline


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path, output_path):
    """Segment brain vessels in DSA image"""
    repo_dir = Path(__file__).parent
    segment = SegmentPipeline(input_path, output_path, repo_dir)
    segment.run()
