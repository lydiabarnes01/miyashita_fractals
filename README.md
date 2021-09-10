### Miyashita Fractals

<p align="center">
  <img src="https://github.com/mrernst/miyashita_fractals/blob/main/imgs/0.png" width="175">
  <img src="https://github.com/mrernst/miyashita_fractals/blob/main/imgs/1.png" width="175">
  <img src="https://github.com/mrernst/miyashita_fractals/blob/main/imgs/2.png" width="175">

#### Information

This is a python reimplementation of the stimuli used in Miyashita, Y. (1988). Neuronal correlate of visual associative long-term memory in the primate temporal cortex. Nature, 335(6193), 817-820. 

 In order to use it you need to have the following packages installed.

* [numpy](http://www.numpy.org/)
* [Pillow](https://pillow.readthedocs.io/)


#### Usage

To use the network simply clone the repository and start with
python3 fractal_generator.py

In order to tweak the parameters like number of stimuli, image size etc. take a look at the arguments to fractal_generator.py.

python3 reconnet.py --imgsize 256 --stimuli 10

for example generates 10 images of size 256x256.