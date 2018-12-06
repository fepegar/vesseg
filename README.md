# Vesseg

Brain vessel segmentation from digital subtraction angiography (DSA) using a 3D convolutional neural network (CNN).

![screenshot](screenshots/slicer.gif)
(Brain parcellation performed using [GIF](https://spiral.imperial.ac.uk/bitstream/10044/1/30755/4/07086081.pdf), not included in this repository).

## Installation

### GPU support

This package uses [NiftyNet](http://www.niftynet.io/), which is built on top of [TensorFlow](https://www.tensorflow.org/), so first of all you need to follow the [instructions to setup your NVIDIA GPU](https://www.tensorflow.org/install/gpu).

### `vesseg` package

Using [`conda`](https://conda.io/docs/) is recommended:

```shell
$ conda create -n vesseg python=3.6 -y  # tensorflow doesn't support python 3.7 yet
$ conda activate vesseg
(vesseg) $ git clone https://github.com/fepegar/vesseg.git --depth 1
$ pip install --editable ./vesseg
```

## Usage

```shell
$ conda activate vesseg
(vesseg) $ vesseg --help
Usage: vesseg [OPTIONS] INPUT_PATH OUTPUT_PATH

  Segment brain vessels in DSA image

Options:
  --help  Show this message and exit.
```

Tested on Linux and macOS.
