the Bnn-inspector is a python gui to analyze atmospheric
particle size distributions. 
Its goal are to
 - visualize the data interactively 
 - analyze new particle formation events
 
it is based on pyqtgraph and heavily used the concept of flowchart and nodes described there. 

it is blazing fast! 

## installation
### mac 
```shell
brew install pyqt@5
conda create -n bnn
conda activate bnn
conda install conda-build
git clone https://github.com/daliagachc/banana-inspector.git
conda develop /opt/homebrew/Cellar/pyqt@5/5.15.4_2/lib/python3.9/site-packages/PyQt5

conda install pip
python -m pip install git+https://github.com/pyqtgraph/pyqtgraph.git
conda install --file banana-inspector/requirements.txt

```