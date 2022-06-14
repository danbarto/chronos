# chronos
MIP timing physics studies


## Setup

FWLite part runs in CMSSW 12 (which is finally python3!):

``` shell
cmsrel CMSSW_12_2_0
cd CMSSW_12_2_0/src

git clone --branch py3 git@github.com:danbarto/RootTools.git

git clone git@github.com:danbarto/chronos.git
```


### Conda environment

#### Setting up miniconda

Skip this part if you already have conda running on uaf.

From within your home directory on the uaf, follow the below instructions to set up the tools to run coffea.
We do this in a virtual environment, using the miniconda environment management package.
You might get some error messages about packages that couldn't get uninstalled that you (usually) can ignore.

```
curl -O -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b 
```

Add conda to the end of ~/.bashrc, so relogin after executing this line
```
~/miniconda3/bin/conda init
```

Stop conda from activating the base environment on login
```
conda config --set auto_activate_base false
conda config --add channels conda-forge
```

Install package to tarball environments
```
conda install --name base conda-pack -y
```

#### Setting up the environments

Create environments with as much stuff from anaconda
```
conda create --name timing python=3.9.7 ipython uproot boost-histogram coffea jupyter -y
``` 

In order to use jupyter you need to run the following:

```
python -m ipykernel install --user --name=timing
jupyter nbextension install --py widgetsnbextension --user
jupyter nbextension enable widgetsnbextension --user --py
```

In order to use jupyter notebooks, log into uaf with

``` shell
ssh YOUR_USER@uaf-10.t2.ucsd.edu -L 8007:localhost:8007
```

Then on the uaf

``` shell
( conda activate timing && jupyter notebook --no-browser --port 8007 )
```



### CMS environment

To work with CMSSW / FWLite, cmsenv needs to be set (currently not needed!):

``` shell
scram b -j 8

cmsenv
```



## Data exploration

### Plotting with coffea / uproot / mplhep

Some code to play with is in `studies`


## Sample production



