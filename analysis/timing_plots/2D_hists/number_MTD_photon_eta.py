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


#get number of cells:
MTDnCells = ak.to_numpy(ak.flatten(events['reco_photon_MTDnCells']))
MTDnClus = ak.to_numpy(ak.flatten(events['reco_photon_MTDnClus']))
reco_photon_eta = np.absolute(ak.to_numpy(ak.flatten(events['reco_photon_eta'])))

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(12,6)) #sublot not necesssary

MTDbins=(20,20)

plt.title("Number of MTD hits per Event vs Reco Photon Eta")
ax1.hist2d(reco_photon_eta, MTDnCells, bins=MTDbins, range=[[0,3],[0,max(MTDnCells)]])
ax1.set_xlabel('reco photon eta')
ax1.set_ylabel('number of MTD cells')

ax2.hist2d(reco_photon_eta, MTDnClus, bins=MTDbins, range=[[0,3],[0,max(MTDnCells)]])
ax2.set_xlabel('reco photon eta')
ax2.set_ylabel('number of MTD clusters')

finalizePlotDir('/home/users/hswanson13/public_html/2Dhists')
fig.savefig('/home/users/hswanson13/public_html/2Dhists/number_of_MTD_photon_eta.png')