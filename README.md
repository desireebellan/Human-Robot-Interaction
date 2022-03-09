# HRI_project

## Requirements

* Ubuntu 16.04
* python2==python2.7
* python3==python3.7

To install pip2 and pip3

```
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py 
sudo python2 get-pip.py
sudo rm get-pip-py
wget https://bootstrap.pypa.io/pip/3.7/get-pip.py 
sudo python3 get-pip.py
sudo rm get-pip.py
```
## Instructions
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
* Add your path to Java folder in final/utility.py
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
cd HRI_project/final
wget https://nlp.stanford.edu/software/stanford-ner-4.2.0.zip
mv stanford-ner-4.2.0.zip stanford-ner.zip
unzip stanford-ner
```
## Solved Issues
If punkt.zip is not downloading properly, try
```
cd ~
mkdir -p nltk_data/tokenizers && cd nltk_data/tokenizers
wget https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip
unzip punkt.zip

```
