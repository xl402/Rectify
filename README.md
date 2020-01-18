# Rectify
### Project for HackCambridge 101 18th-19th January, 2020
#### Participants: *Luke Andrews, Rory Xiao, Adian Liusie, Vyas Raina and Tom Lu*

## Set-up:
* Clone by running: `git clone https://github.com/xl402/Rectify.git`
* After cloning, run: `conda env create -f environment.yml`
* Ask for `secrete.json` containing gmail login and passowrds, and store at root directory
* Create gitignore file `.gitignore` and add entry `secret.json`


Pre-trained models to install:
a) For object detection: https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/
b) For image prediction: https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/

general instructions in (https://readthedocs.org/projects/imageai/downloads/pdf/latest/)

To run above need exactly the following packages:

1) tensorflow==1.14.0
2) opencv-python
3) keras
4) imageai --upgrade
