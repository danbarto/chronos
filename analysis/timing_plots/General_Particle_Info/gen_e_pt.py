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
events0mm = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing0mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events() 

events100mm = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()


events = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing1000mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()


#get gen electron times for 0mm, 100mm, 1000mm
ge_pt = events['e_pt']

ge_pt100 = events100mm['e_pt']

ge_pt0 = events0mm['e_pt']


bin_start = 0
bin_end = 150
n_bins = 30
bin_width = (bin_end - bin_start)/n_bins


names = [r'$c\tau$=1000mm',r'$c\tau$=100mm',r'$c\tau$=0mm']
colors = ['b','r','g']

arrs = [ak.flatten(ge_pt),ak.flatten(ge_pt100),ak.flatten(ge_pt0)]
xlabel = r'Gen Ele $p_T (GeV/c)'
binning = np.linspace(bin_start,bin_end,n_bins)
histograms = []
for arr in arrs:
    hist = bh.Histogram(bh.axis.Variable(binning), storage=bh.storage.Weight(),)
    hist.fill(arr, weight=np.ones_like(arr),)
    area = sum(hist.counts()) #bin_width*hist.counts(), guess not! haha works
    histograms.append(hist)

fig, ax = plt.subplots(figsize=(8, 8))
hep.histplot([hist.counts() for hist in histograms],
        binning,
        histtype="step",
        stack=False,
        label=[fr'$h\to XX\to 4e$: {name}' for name in names],
        color=colors,
        ax=ax,)

hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

ax.set_ylabel(r'Counts')
ax.set_xlabel(xlabel, fontsize=18)
plt.legend(loc=0)
finalizePlotDir('/home/users/hswanson13/public_html/General_Particle_Info/')

fig.savefig('/home/users/hswanson13/public_html/General_Particle_Info/gen_e_pt.png')