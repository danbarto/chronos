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
events= NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()

reco_photon_pt = events['reco_photon_pt']
reco_photon_eta = events['reco_photon_eta']
reco_photon_phi = events['reco_photon_phi']
reco_photon_M = np.zeros_like(reco_photon_pt)

gen_e_pt = events['e_pt']
gen_e_eta = events['e_eta']
gen_e_phi = events['e_phi']
gen_e_M = np.zeros_like(gen_e_pt)

#make 4vectors
reco_photon_vec4 = ak.zip(
    {
        "pt": reco_photon_pt,
        "eta": reco_photon_eta,
        "phi": reco_photon_phi,
        "mass": reco_photon_M,
    },
    with_name="PtEtaPhiMLorentzVector",
)

gen_e_vec4 = ak.zip( 
    {
        "pt": gen_e_pt,
        "eta": gen_e_eta,
        "phi": gen_e_phi,
        "mass": gen_e_M,
    },
    with_name="PtEtaPhiMLorentzVector",
)

photon_e_combo = ak.cartesian([reco_photon_vec4, gen_e_vec4]) #not nested, axis=1

#Create a mask, True if less than 0.4 and True if more
mask = delta_r(photon_e_combo['0'], photon_e_combo['1']) < 0.4

#applying the mask, same dims as the combo but False just removes the ones w <0.4 dR
matched_photons_e = photon_e_combo[mask]
matched_photons = matched_photons_e['0'] #0 gets the photons
matched_e = matched_photons_e['1'] #1 gets the electrons, bec of cartesian order


#Calculate the perc
match_perc = ak.flatten((matched_photons.pt - matched_e.pt)/matched_e.pt)


bin_start = -1
bin_end = 1 
n_bins = 30
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=100mm'
color='b'

arr = match_perc
xlabel = r'$p_T$ - gen_e_$p_T$ / gen_e_$p_T$' 
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
plt.legend(loc=0)
finalizePlotDir('/home/users/hswanson13/public_html/matching_photons/')

fig.savefig('/home/users/hswanson13/public_html/matching_photons/pt_match_photons.png')