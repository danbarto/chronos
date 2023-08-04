import warnings
warnings.filterwarnings("ignore")

import numpy as np
import coffea

from coffea.nanoevents import NanoEventsFactory, BaseSchema

import matplotlib.pyplot as plt
import mplhep as hep #matplotlib wrapper for easy plotting in HEP
plt.style.use(hep.style.CMS)

import awkward as ak #just lets you do lists but faster i guess

from coffea.nanoevents.methods import vector
ak.behavior.update(vector.behavior)

import boost_histogram as bh

#import os
# os.chdir(r"/home/users/hswanson13/CMSSW_12_2_0/src/chronos/Tools/")
# from helpers.py import *
# os.chdir(r"/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots")

#from .helpers import cross

#!/usr/bin/env python3
import os

def get_four_vec_fromPtEtaPhiM(cand, pt, eta, phi, M, copy=True):
    '''
    Get a LorentzVector from a NanoAOD candidate with custom pt, eta, phi and mass
    All other properties are copied over from the original candidate
    '''
    from coffea.nanoevents.methods import vector
    ak.behavior.update(vector.behavior)

    vec4 = ak.zip(
        {
            "pt": pt,
            "eta": eta,
            "phi": phi,
            "mass": M,
        },
        with_name="PtEtaPhiMLorentzVector",
    )
    if copy:
        vec4.__dict__.update(cand.__dict__)
    return vec4

def delta_phi(first, second):
    return np.arccos(np.cos(first.phi - second.phi))

def delta_r2(first, second):
    return (first.eta - second.eta) ** 2 + delta_phi(first, second) ** 2

def delta_r(first, second):
    return np.sqrt(delta_r2(first, second))

def choose(first, n=2):
    tmp = ak.combinations(first, n)
    combs = tmp['0']
    for i in range(1,n):
        combs = combs.__add__(tmp[str(i)])
    for i in range(n):
        combs[str(i)] = tmp[str(i)]
    return combs

def cross(first, second):
    tmp = ak.cartesian([first, second])
    combs = (tmp['0'] + tmp['1'])
    combs['0'] = tmp['0']
    combs['1'] = tmp['1']
    return combs

def match(first, second, deltaRCut=0.4):
    drCut2 = deltaRCut**2
    combs = ak.cartesian([first, second], nested=True)
    return ak.any((delta_r2(combs['0'], combs['1'])<drCut2), axis=2)

def finalizePlotDir( path ):
    path = os.path.expandvars(path)
    if not os.path.isdir(path):
        os.makedirs(path)
    shutil.copy( os.path.expandvars( '$TIMEHOME/Tools/php/index.php' ), path )
