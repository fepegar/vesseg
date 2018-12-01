from pathlib import Path
from csv import DictWriter
from subprocess import call
from shutil import rmtree, copytree
from configparser import ConfigParser


WEIGHTS_URL = (
    'https://github.com/fepegar/vesseg-models/'
    'blob/master/models/model_scaling.tar.gz?raw=true'
)

NETWORK_IMPORT_STRING = (
    'vesseg_networks'
    '.highres3dnet_smaller'
    '.HighRes3DNetSmaller'
)


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


    def copy_networks_dir(self, repo_dir):
        networks_dir = repo_dir / 'vesseg' / 'networks'
        niftynet_home_dir = Path.home() / 'niftynet'
        niftynet_networks_dir = Path(
            niftynet_home_dir,
            'niftynetext',
            'network',
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


    def run(self):
        self.download_weights()
        self.make_csv()
        self.make_config()
        self.infer()


def get_nifti_stem(path):
    return path.stem.replace('.nii', '')
