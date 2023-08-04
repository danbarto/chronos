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


#get data of events
track_pt = events['track_pt']
track_eta = events['track_eta']
track_phi = events['track_phi']
track_M = np.zeros_like(track_pt)

gen_e_pt = events['e_pt']
gen_e_eta = events['e_eta']
gen_e_phi = events['e_phi']
gen_e_M = np.zeros_like(gen_e_pt)

#make 4vectors
track_vec4 = ak.zip(
    {
        "pt": track_pt,
        "eta": track_eta,
        "phi": track_phi,
        "mass": track_M,
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

track_e_combo = ak.cartesian([track_vec4, gen_e_vec4]) #not nested, axis=1

#Create a mask, True if less than 0.4 and True if more
te_mask = delta_r(track_e_combo['0'], track_e_combo['1']) < 0.4

#applying the mask, same dims as the combo but False just removes the ones w <0.4 dR
matched_track_e = track_e_combo[te_mask]

matched_track = matched_track_e['0'] #0 gets the photons
matched_e = matched_track_e['1'] #1 gets the electrons, bec of cartesian order

#Calculate the perc
match_perc = ak.flatten((matched_track.pt - matched_e.pt)/matched_e.pt)


bin_start = -1
bin_end = 1 
n_bins = 70
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
finalizePlotDir('/home/users/hswanson13/public_html/matching_tracks/')

fig.savefig('/home/users/hswanson13/public_html/matching_tracks/pt_match_tracks.png')