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

from matplotlib.lines import Line2D


events100mm = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()
events0mm = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing0mm.root',
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

def match_photons(mtd_vec4,eta_hits, phi_hits, photon_vec4,dR):
    mp_cart = ak.cartesian([mtd_vec4, photon_vec4]) #not nested, axis=1

    #met_cart = ak.cartesian([mtd_vec4, eta_hits]) 
    #mph_cart = ak.cartesian([mtd_vec4, phi_hits])

    dRmask = np.absolute(delta_r(mp_cart['0'], mp_cart['1'])) < dR 
    
    mch_p_eta = (mp_cart[dRmask])['1'].eta
    mch_p_phi = (mp_cart[dRmask])['1'].phi

    mch_phi = (mp_cart[dRmask])['0'].phi 
    mch_eta = (mp_cart[dRmask])['0'].eta  

    return [mch_eta, mch_phi, mch_p_eta, mch_p_phi]

#run the function for all btl, etl events!
dR = 0.4
etl_mch0 = match_photons(mtd_etl_vec40, eta_etl_hits0, phi_etl_hits0, reco_photon_vec40, dR)
etl_mch100 = match_photons(mtd_etl_vec4100, eta_etl_hits100, phi_etl_hits100, reco_photon_vec4100, dR)
etl_mch = match_photons(mtd_etl_vec4, eta_etl_hits, phi_etl_hits, reco_photon_vec4, dR)
etl_matches = [etl_mch0, etl_mch100, etl_mch]

btl_mch0 = match_photons(mtd_btl_vec40, eta_btl_hits0, phi_btl_hits0, reco_photon_vec40, dR)
btl_mch100 = match_photons(mtd_btl_vec4100, eta_btl_hits100, phi_btl_hits100, reco_photon_vec4100, dR)
btl_mch = match_photons(mtd_btl_vec4, eta_btl_hits, phi_btl_hits, reco_photon_vec4, dR)
btl_matches = [btl_mch0, btl_mch100, btl_mch]

all_eta_etl_hits = [eta_etl_hits0,eta_etl_hits100,eta_etl_hits]
all_phi_etl_hits = [phi_etl_hits0,phi_etl_hits100,phi_etl_hits]

all_eta_btl_hits = [eta_btl_hits0,eta_btl_hits100,eta_btl_hits]
all_phi_btl_hits = [phi_btl_hits0,phi_btl_hits100,phi_btl_hits]

#Remember its per event, the amount of hits
counter = 0
s_n = 1 #sample number 0 for 0mm, 1 for 100mm, 2 for 1000mm    

for event in range(len(eta_etl_hits100)):
    #fig.patch.set_facecolor('#ADD8E6')
    plt.title(fr'$c\tau$=100mm $h\to XX\to 4e$: Eta vs Phi for Event {counter}', fontsize = 18)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax = fig.gca()
    #plot all hits from mtd
    plt.scatter(ak.to_numpy(all_eta_etl_hits[s_n][event]), ak.to_numpy(all_phi_etl_hits[s_n][event]), c='grey', s=8)
    plt.scatter(ak.to_numpy(all_eta_btl_hits[s_n][event]), ak.to_numpy(all_phi_btl_hits[s_n][event]), c='grey', s=8)
    #plot all matched mtd hits
    plt.scatter(ak.to_numpy(etl_matches[s_n][0][event]), ak.to_numpy(etl_matches[s_n][1][event]), c='red', s=8)
    plt.scatter(ak.to_numpy(btl_matches[s_n][0][event]), ak.to_numpy(btl_matches[s_n][1][event]), c='red', s=8)
    #plot photon matches
    plt.scatter(ak.to_numpy(etl_matches[s_n][2][event]), ak.to_numpy(etl_matches[s_n][3][event]), c='blue', s=8)
    plt.scatter(ak.to_numpy(btl_matches[s_n][2][event]), ak.to_numpy(btl_matches[s_n][3][event]), c='blue', s=8)
    

    #print(f'before loop: {counter}')
    for emEta,emPhi in zip(etl_matches[s_n][2][event], etl_matches[s_n][3][event]):
        eCircle = plt.Circle((emEta, emPhi), 0.4, color='black', fill=False,clip_on=True)
        #print(f'inner loop 1 {counter}')
        #print(len(etl_matches[s_n][0][event]))
        ax.add_patch(eCircle)

    for bmEta,bmPhi in zip(btl_matches[s_n][2][event], btl_matches[s_n][3][event]):
        bCircle = plt.Circle((bmEta, bmPhi), 0.4, color='black', fill=False,clip_on=True)
        ax.add_patch(bCircle)
        #print(f'inner loop 2 {counter}')
        #print(len(etl_matches[s_n][0][event]))
        
    #print(f'after loop {counter}')
    
    #plt.legend([r"all hits", r"all hits", r"matched mtd hits"], ncol = 1 , loc = "upper right", markerscale = 5,frameon=True,fancybox=True)
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='All MTD Hits', markerfacecolor='grey', markersize=15),
                       Line2D([0], [0], marker='o', color='w', label='Matched MTD Hits', markerfacecolor='red', markersize=15),
                       Line2D([0], [0], marker='o', color='w', label='Matched Photon Hits', markerfacecolor='blue', markersize=15)]

    ax.legend(handles=legend_elements,loc='upper right')
    finalizePlotDir('/home/users/hswanson13/public_html/MTD_timing_hists/MTD_eta_phi_plots/')
    fig.savefig(f'/home/users/hswanson13/public_html/MTD_timing_hists/MTD_eta_phi_plots/MTD_eta_phi_{str(counter)}.png')
    fig.clear()
    counter += 1
    if counter == 5:
        break

print('hi')