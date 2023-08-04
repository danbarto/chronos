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

e_vx = events['e_vx']
e_vy = events['e_vy']
e_vz = events['e_vz']

e_R = np.sqrt(e_vx**2 + e_vy**2 + e_vz**2)
max_e_R = [max(i) for i in e_R]

n_reco_photon = ak.to_numpy(ak.Array([len(i) for i in events['reco_photon_pt']]))

fig, ax = plt.subplots(figsize=(8, 8))

plt.title(fr"CMS Preliminary: $c\tau$=100mm")
plt.hist2d(n_reco_photon, max_e_R, bins=(9,9))
plt.colorbar()
plt.xlabel('number of photons per event')
plt.ylabel('maximum LLP vertex displacement')

finalizePlotDir('/home/users/hswanson13/public_html/2Dhists')
fig.savefig('/home/users/hswanson13/public_html/2Dhists/disp_gen_e_reco_photon.png')
