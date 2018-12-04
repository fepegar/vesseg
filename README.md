# Vesseg
Brain vessel segmentation from digital subtraction angiography (DSA) using a 3D convolutional neural network (CNN).

![](screenshots/slicer.gif)
(Brain parcellation performed using [GIF](https://spiral.imperial.ac.uk/bitstream/10044/1/30755/4/07086081.pdf), not included in this repository).

## Installation
### GPU support
This package uses [NiftyNet](http://www.niftynet.io/), which is built on top of [TensorFlow](https://www.tensorflow.org/), so first of all you need to follow the [instructions to setup your NVIDIA GPU](https://www.tensorflow.org/install/gpu).

### `vesseg` package
```shell
$ pip install git+https://github.com/fepegar/vesseg
```


## Usage
```shell
$ vesseg --help
Usage: vesseg [OPTIONS] INPUT_PATH OUTPUT_PATH

  Segment brain vessels in DSA image

Options:
  --help  Show this message and exit.

```
