from pathlib import Path
from csv import DictWriter
from subprocess import call
from tempfile import mkdtemp
from shutil import rmtree, copytree
from configparser import ConfigParser

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
