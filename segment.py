from pathlib import Path
from shutil import rmtree
from csv import DictWriter
from subprocess import call
from tempfile import mkdtemp
from configparser import ConfigParser

import click

this_dir = Path(__file__).parent
config_template_path = this_dir / 'config_template.ini'

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--cleanup', default=False)
@click.option('--verbose', default=True)
def segment(input_path, output_path, cleanup, verbose):
    """Segment DSA image"""
    input_path = Path(input_path)
    output_path = Path(output_path)
    tempdir = get_tempdir(input_path)
    if verbose:
        click.echo(f'Directory "{tempdir}" created')
    csv_path, ini_path = get_config_paths(tempdir)
    download_weights()
    make_csv(input_path, csv_path)
    make_config(config_template_path, csv_path, output_path, ini_path)
    infer(ini_path)

    if cleanup:
        if verbose:
            click.echo(f'Removing "{tempdir}"...')
        rmtree(tempdir)


def get_nifti_stem(path):
    return path.stem.replace('.nii', '')


def get_tempdir(input_path):
    prefix = f"{get_nifti_stem(input_path)}__"
    tempdir = mkdtemp(prefix=prefix)
    return Path(tempdir)


def get_config_paths(output_dir):
    csv_path = output_dir / 'input.csv'
    ini_path = output_dir / 'config.ini'
    return csv_path, ini_path


def download_weights():
    return


def make_csv(input_path, csv_path):
    with open(csv_path, 'w') as csvfile:
        fieldnames = ['image_id', 'image_path']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(
            {'image_id': get_nifti_stem(input_path), 'image_path': input_path}
        )


def make_config(template_path, csv_path, output_path, ini_path):
    config = ConfigParser()
    config.read(template_path)
    config['DSA']['csv_file'] = str(csv_path)
    config['SYSTEM']['model_dir'] = str(None)  # TODO
    config['NETWORK']['name'] = str(None)  # TODO
    config['INFERENCE']['save_seg_dir'] = str(output_path.parent)
    with open(ini_path, 'w') as configfile:
        config.write(configfile)


def infer(config_path):
    command = [
        'net_segment',
        '-c', str(config_path),
        'inference',
    ]
    print(' '.join(command))
    # call(command)
