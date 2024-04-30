# Emotion Game

## Table of Contents
- [Emotion Game](#Emotion-Game)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  
## Description
## Installation
### Requirements

* Ubuntu 16.04
* python2==python2.7
* python3==python3.7

Check the required packages in the file [requirements3.txt](requirements3.txt) for python3 and [requirements2.txt](requirements2.txt) for python2. 

To install pip2 and pip3

```
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py 
sudo python2 get-pip.py
sudo rm get-pip.py
wget https://bootstrap.pypa.io/pip/get-pip.py 
sudo python3 get-pip.py
sudo rm get-pip.py
```
### Setup
Copy the reporitory locally

```
git clone https://github.com/desireebellan/HRI_project.git
```
To use the library nltk.tag.stanford.StandfordNERTagger you need to execute the following instructions:
* Install Java
```
sudo apt-get install default-jdk
```
* Add your path to Java folder in [emotionPepper/dialogue.py](emotionPepper/dialogue.py)
* Install nltk
```
pip2 install nltk==3.4
```
* Download and unzip the package punkt:
```
cd ~
mkdir -p nltk_data/tokenizers && cd nltk_data/tokenizers
wget https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.zip?raw=true
mv punkt.zip?raw=true punkt.zip
unzip punkt.zip
```
* Download and unzip the folder stenford-ner:
```
cd HRI_project/emotionPepper
wget https://nlp.stanford.edu/software/stanford-ner-4.2.0.zip
mv stanford-ner-4.2.0.zip stanford-ner.zip
unzip stanford-ner
```
* Download the folder model_data [here](https://drive.google.com/uc?id=1Jjjq2LOyrwcQRIZAhU-ZA0IyvQ7NPLAi&export=download) and unzip it inside HRI_project/emotionPepper
* Download the packages naoqi and pynaoqi

## Usage
### Launh the app
* Open naoqi
```
cd ~/naosoftware/naoqi
./naoqi
```
* Open Choregraphe and connect to the local server (IP: 127.00...., PORT: 9959....)
* On a different terminal launch the app
```
python3.7 app.py
```
## Solved Issues

* If punkt.zip is not downloading properly, try
```
cd ~
mkdir -p nltk_data/tokenizers && cd nltk_data/tokenizers
wget https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip
unzip punkt.zip
```
* To install python3.7 on ubuntu16.04
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7
```
## Contributing
## Licence
## Acknowledgements

