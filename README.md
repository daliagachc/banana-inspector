![image](https://user-images.githubusercontent.com/15239248/135803333-d86d1643-6b83-4f9d-801c-b596733318a9.png)


the Bnn-inspector is a python gui to analyze atmospheric
particle size distributions. 
Its goal are to
 - visualize the data interactively 
 - analyze new particle formation events
 
it is based on pyqtgraph and heavily used the concept of flowchart and nodes described there. 

it is blazing fast! 

## installation

### linux
```shell
conda create -n bnn
conda activate bnn
conda install conda-build
conda install pip

conda install --file banana-inspector/requirements_linux.txt

#install latest pyqtgraph from github 
python -m pip install git+https://github.com/pyqtgraph/pyqtgraph.git


git clone git+https://github.com/daliagachc/banana-inspector.git
conda develop banana-inspector

```


### mac air with m1 chip 
```shell
# depending on your mac you can install PyQt5 directly from conda
brew install pyqt@5
conda create -n bnn
conda activate bnn
conda install conda-build
git clone https://github.com/daliagachc/banana-inspector.git
conda develop /opt/homebrew/Cellar/pyqt@5/5.15.4_2/lib/python3.9/site-packages/PyQt5

conda install pip
python -m pip install git+https://github.com/pyqtgraph/pyqtgraph.git
conda install --file banana-inspector/requirements_mac.txt

```

## basi usage: 

```shell
conda activate bnn 
cd banana-inspector/examples
# try any of the following 
python 
```
=======
![banana-inspector](https://user-images.githubusercontent.com/15239248/135773459-d1e0a308-5cb7-40f1-af52-069ef922c623.gif)


