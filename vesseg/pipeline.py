from pathlib import Path
from csv import DictWriter
from subprocess import call
from shutil import rmtree, copytree
from configparser import ConfigParser

from.processing import remove_small_components

WEIGHTS_URL = (
    'https://github.com/fepegar/vesseg-models/'
    'blob/master/models/model_scaling.tar.gz?raw=true'
)

NETWORK_IMPORT_STRING = (
    'vesseg_networks'
    '.highres3dnet_smaller'
    '.HighRes3DNetSmaller'
)

OUTPUT_SUFFIX = '_vesseg'


class SegmentPipeline:
    def __init__(self, input_path, output_path, repo_dir):
        self.input_path = Path(input_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.copy_networks_dir(repo_dir)
        self.vesseg_home_dir = Path.home() / '.vesseg'
        self.model_dir = self.vesseg_home_dir / 'model'
        self.config_template_path = repo_dir / 'config_template.ini'
        self.csv_path = self.vesseg_home_dir / 'input.csv'
        self.config_path = self.vesseg_home_dir / 'config.ini'
        self.remove_small_components = True


    def copy_networks_dir(self, repo_dir):
        networks_dir = repo_dir / 'vesseg' / 'networks'
        niftynet_home_dir = Path.home() / 'niftynet'
        niftynet_networks_dir = Path(
            niftynet_home_dir,
            'extensions',
            'vesseg_networks',
        )
        niftynet_networks_dir.mkdir(parents=True, exist_ok=True)
        rmtree(niftynet_networks_dir)
        copytree(networks_dir, niftynet_networks_dir)


    def download_weights(self):
        if not self.model_dir.is_dir():
            from niftynet.utilities.download import download_and_decompress
            download_and_decompress(WEIGHTS_URL, self.model_dir / 'models')


    def make_csv(self):
        with open(self.csv_path, 'w') as csvfile:
            fieldnames = ['image_id', 'image_path']
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'image_id': get_nifti_stem(self.input_path),
                'image_path': self.input_path,
            })


    def make_config(self):
        config = ConfigParser()
        config.read(self.config_template_path)
        config['DSA']['csv_file'] = str(self.csv_path)
        config['SYSTEM']['model_dir'] = str(self.model_dir)
        config['NETWORK']['name'] = NETWORK_IMPORT_STRING
        config['INFERENCE']['save_seg_dir'] = str(self.vesseg_home_dir)
        config['INFERENCE']['output_postfix'] = OUTPUT_SUFFIX
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)


    def infer(self):
        command = [
            'net_segment',
            'inference',
            '-c', str(self.config_path),
        ]
        print('Running NiftyNet command:')
        print(' '.join(command))
        call(command)


    def get_default_output_path(self):
        default_output_path = (
            self.vesseg_home_dir
            / self.input_path.name.replace('.nii', f'{OUTPUT_SUFFIX}.nii')
        )
        return default_output_path


    def postprocess(self):
        default_output_path = self.get_default_output_path()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        default_output_path.rename(self.output_path)
        if self.remove_small_components:
            remove_small_components(self.output_path)


    def run(self):
        self.download_weights()
        self.make_csv()
        self.make_config()
        self.infer()
        self.postprocess()


def get_nifti_stem(path):
    return path.stem.replace('.nii', '')
