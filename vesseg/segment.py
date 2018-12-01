from pathlib import Path
from csv import DictWriter
from subprocess import call
from tempfile import mkdtemp
from shutil import rmtree, copytree
from configparser import ConfigParser

import click

this_dir = Path(__file__).parent
config_template_path = this_dir / 'config_template.ini'
networks_dir = this_dir / 'networks'
network_import_string = 'networks.highres3dnet_smaller.HighRes3DNetSmaller'

niftynet_networks_dir = Path(
    Path.home(), '.niftynet', 'niftynetext', 'network', 'networks')

niftynet_networks_dir.mkdir(parents=True, exist_ok=True)
rmtree(niftynet_networks_dir)
copytree(networks_dir, niftynet_networks_dir)

vesseg_dir = Path.home() / 'vesseg'
model_dir = vesseg_dir / 'model'
WEIGHTS_URL = (
    'https://github.com/fepegar/vesseg-models/'
    'blob/master/models/model_scaling.tar.gz?raw=true'
)


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
    if not model_dir.is_dir():
        from niftynet.utilities.download import download_and_decompress
        download_and_decompress(WEIGHTS_URL, model_dir / 'models')


def make_csv(input_path, csv_path):
    with open(csv_path, 'w') as csvfile:
        fieldnames = ['image_id', 'image_path']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(
            {'image_id': get_nifti_stem(input_path), 'image_path': input_path}
        )


def make_config(template_path, csv_path, output_dir, ini_path):
    config = ConfigParser()
    config.read(template_path)
    config['DSA']['csv_file'] = str(csv_path)
    config['SYSTEM']['model_dir'] = str(model_dir)
    config['NETWORK']['name'] = network_import_string
    config['INFERENCE']['save_seg_dir'] = str(output_dir)
    with open(ini_path, 'w') as configfile:
        config.write(configfile)


def infer(config_path):
    command = [
        'net_segment',
        '-c', str(config_path),
        'inference',
    ]
    print('Running NiftyNet command:')
    print(' '.join(command))
    call(command)


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path, output_path):
    """Segment DSA image"""
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    csv_path, ini_path = get_config_paths(vesseg_dir)
    download_weights()
    make_csv(input_path, csv_path)
    make_config(config_template_path, csv_path, vesseg_dir, ini_path)
    infer(ini_path)
