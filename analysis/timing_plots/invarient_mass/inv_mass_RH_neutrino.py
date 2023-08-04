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

from Tools.helpers import get_four_vec_fromPtEtaPhiM, delta_phi, cross, delta_r, delta_r2, choose, match, finalizePlotDir
events = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()

pt = events['LLP_pt']
eta = events['LLP_eta']
phi = events['LLP_phi']
m = np.zeros_like(pt)
vec4 = ak.zip( #vec4 this will get the four vector of whatever you give it
    {
        "pt": pt,
        "eta": eta,
        "phi": phi,
        "mass": m,
    },
    with_name="PtEtaPhiMLorentzVector",
)


inv_mass = (vec4[:,0] + vec4[:,1]).mass

bin_start = 0
bin_end = 100
n_bins = 10
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=100mm'
color='b'

arr = inv_mass
xlabel = 'Invarient Mass of RH Neutrino'
binning = np.linspace(bin_start,bin_end,n_bins)
hist = bh.Histogram(bh.axis.Variable(binning), storage=bh.storage.Weight(),)
hist.fill(arr, weight=np.ones_like(arr),)

fig, ax = plt.subplots(figsize=(8, 8))
hep.histplot([hist.counts(),],
        binning,
        histtype="step",
        stack=False,
        label=fr'$h\to XX\to 4e$: {name}',
        color=color,
        ax=ax,)

hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

ax.set_ylabel(r'Counts')
ax.set_xlabel(xlabel, fontsize=18)
plt.legend(loc=2)
finalizePlotDir('/home/users/hswanson13/public_html/invarient_mass/')

fig.savefig('/home/users/hswanson13/public_html/invarient_mass/inv_mass_RH_neutrino.png')
