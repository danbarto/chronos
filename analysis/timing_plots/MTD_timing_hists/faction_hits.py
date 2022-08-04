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


#get reco photon times for 0mm, 100mm, 1000mm
reco_photon_pt = events['reco_photon_pt']
reco_photon_eta = events['reco_photon_eta']
reco_photon_phi = events['reco_photon_phi']
reco_photon_M = np.zeros_like(reco_photon_pt)

reco_photon_pt100 = events100mm['reco_photon_pt']
reco_photon_eta100 = events100mm['reco_photon_eta']
reco_photon_phi100 = events100mm['reco_photon_phi']
reco_photon_M100 = np.zeros_like(reco_photon_pt100)

reco_photon_pt0 = events0mm['reco_photon_pt']
reco_photon_eta0 = events0mm['reco_photon_eta']
reco_photon_phi0 = events0mm['reco_photon_phi']
reco_photon_M0 = np.zeros_like(reco_photon_pt0)

#etl hits
eta_etl_hits100 = events100mm['gp_eta_etl_hits']
phi_etl_hits100 = events100mm['gp_phi_etl_hits']
eta_etl_hits0 = events0mm['gp_eta_etl_hits']
phi_etl_hits0 = events0mm['gp_phi_etl_hits']
eta_etl_hits = events['gp_eta_etl_hits']
phi_etl_hits = events['gp_phi_etl_hits']

#btl hits
eta_btl_hits100 = events100mm['gp_eta_btl_hits']
phi_btl_hits100 = events100mm['gp_phi_btl_hits']
eta_btl_hits0 = events0mm['gp_eta_btl_hits']
phi_btl_hits0 = events0mm['gp_phi_btl_hits']
eta_btl_hits = events['gp_eta_btl_hits']
phi_btl_hits = events['gp_phi_btl_hits']

#four vectors
reco_photon_vec4100 = ak.zip({"pt": reco_photon_pt100,"eta": reco_photon_eta100,"phi": reco_photon_phi100,"mass": reco_photon_M100,},with_name="PtEtaPhiMLorentzVector",)
reco_photon_vec4 = ak.zip({"pt": reco_photon_pt,"eta": reco_photon_eta,"phi": reco_photon_phi,"mass": reco_photon_M,},with_name="PtEtaPhiMLorentzVector",)
reco_photon_vec40 = ak.zip({"pt":reco_photon_pt0, "eta":reco_photon_eta0, "phi": reco_photon_phi0, "mass":reco_photon_M0,},with_name="PtEtaPhiMLorentzVector",)

mtd_etl_vec4100 = ak.zip({"pt": np.zeros_like(phi_etl_hits100),"eta": eta_etl_hits100,"phi": phi_etl_hits100,"mass" :np.zeros_like(phi_etl_hits100),},with_name="PtEtaPhiMLorentzVector",)
mtd_etl_vec40 = ak.zip({"pt": np.zeros_like(phi_etl_hits0),"eta": eta_etl_hits0,"phi": phi_etl_hits0,"mass" :np.zeros_like(phi_etl_hits0),},with_name="PtEtaPhiMLorentzVector",)
mtd_etl_vec4 = ak.zip({"pt": np.zeros_like(phi_etl_hits),"eta": eta_etl_hits,"phi": phi_etl_hits,"mass" :np.zeros_like(phi_etl_hits),},with_name="PtEtaPhiMLorentzVector",)

mtd_btl_vec4100 = ak.zip({"pt": np.zeros_like(phi_btl_hits100),"eta": eta_btl_hits100,"phi": phi_btl_hits100,"mass" :np.zeros_like(phi_btl_hits100),},with_name="PtEtaPhiMLorentzVector",)
mtd_btl_vec40 = ak.zip({"pt": np.zeros_like(phi_btl_hits0),"eta": eta_btl_hits0,"phi": phi_btl_hits0,"mass" :np.zeros_like(phi_btl_hits0),},with_name="PtEtaPhiMLorentzVector",)
mtd_btl_vec4 = ak.zip({"pt": np.zeros_like(phi_btl_hits),"eta": eta_btl_hits,"phi": phi_btl_hits,"mass" :np.zeros_like(phi_btl_hits),},with_name="PtEtaPhiMLorentzVector",)

#concatenate on the right axis, 1, to merge events together

total_photons = len(ak.flatten(reco_photon_eta))
def frac_photons(mtd_vec4,photon_vec4,total_photons,dR):
    
    mp_cart = ak.cartesian([photon_vec4,mtd_vec4], nested=True) #not nested, axis=1
        
    dRmask = np.absolute(delta_r(mp_cart['0'], mp_cart['1'])) < dR 
    
    #apply mask to cartesian for pairs that dont satisify dR restriction
    filt = mp_cart[dRmask]['0'].eta
    #Count the number of elements in filter, the ones that are NOT empty, >0, means that that was a matched photon!
    num_nest = ak.num(filt, axis=-1) > 0
    #apply filter to photon v4
    match_pho = (photon_vec4[num_nest]).eta

    #count the number of matches in each sub list
    num_match_pho = ak.num(match_pho,axis=-1)
    #sum it up!
    tot_match_photons = sum(num_match_pho)
    # print(tot_match_photons)
    # print(total_photons)
    # print('')
    #now calcultate the fraction
    frac_photon = tot_match_photons/total_photons

    return frac_photon

dR_list = np.arange(0,6.92,0.01)
ef_frac = []
bf_frac = []
counter = 0
for dR in dR_list:
    bf = frac_photons(mtd_btl_vec4,reco_photon_vec4, total_photons,dR)
    bf_frac.append(bf)
    # print(ef)
    # print(bf)
    # print(ef+bf)
    # print('')
    ef = frac_photons(mtd_etl_vec4,reco_photon_vec4, total_photons,dR)
    ef_frac.append(ef)
    counter +=1
    # if counter ==5:
    #     break


fig, ax = plt.subplots(figsize=(8, 8))

plt.title(r'Effeciency Plot: $h\to XX\to 4e$, $c\tau$=1000mm, ', fontsize = 18)
plt.scatter(dR_list,ef_frac,c='red',s=3)
plt.scatter(dR_list,bf_frac,c='blue',s=3)

plt.ylabel(r'Match Photons / Total Photons',fontsize=18)
plt.xlabel('dR', fontsize=18)

plt.legend([r"ETL Efficiency" , r"BTL Efficiency"], ncol = 2, loc="lower right",prop={'size': 12},markerscale=5,frameon=True,fancybox=True)

finalizePlotDir('/home/users/hswanson13/public_html/MTD_timing_hists/')
fig.savefig('/home/users/hswanson13/public_html/MTD_timing_hists/photon_fraction_hits.png')