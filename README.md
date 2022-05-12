# chronos
MIP timing physics studies

## Setup

FWLite part runs in CMSSW 12 (which is finally python3!):

``` shell
cmsrel CMSSW_12_2_0
cd CMSSW_12_2_0/src

git clone --branch py3 git@github.com:danbarto/RootTools.git

git clone git@github.com:danbarto/chronos.git

scram b -j 8

cmsenv
```

Analysis part (hopefully) runs in a more pythonic environment.
To-Do

## Sample production


## Data exploration

Some code to play with is in `studies`

