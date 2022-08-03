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

#make gen e four vectors
reco_photon_vec4 = ak.zip({"pt": reco_photon_pt,"eta": reco_photon_eta,"phi": reco_photon_phi,"mass": reco_photon_M,},with_name="PtEtaPhiMLorentzVector",)
reco_photon_vec4100 = ak.zip({"pt": reco_photon_pt100,"eta": reco_photon_eta100,"phi": reco_photon_phi100,"mass": reco_photon_M100,},with_name="PtEtaPhiMLorentzVector",)
reco_photon_vec40 = ak.zip({"pt":reco_photon_pt0, "eta":reco_photon_eta0, "phi": reco_photon_phi0, "mass":reco_photon_M0,},with_name="PtEtaPhiMLorentzVector",)

#get reco photon timing info for Cell times and Cluster times
# MTDCellTime = events['reco_photon_MTDtime']
MTDCellTime100 = events100mm['reco_photon_MTDtime']
MTDCellTime0 = events0mm['reco_photon_MTDtime']

#get all etl hit info
theta_etl_hits0 = events0mm['gp_theta_etl_hits']
eta_etl_hits0 = events0mm['gp_eta_etl_hits']
phi_etl_hits0 = events0mm['gp_phi_etl_hits']
time_etl_hits0 = events0mm['gp_time_etl_hits']
energy_etl_hits0 = events0mm['gp_energy_etl_hits']
x_etl_hits0 = events0mm['gp_x_etl_hits']
y_etl_hits0 = events0mm['gp_y_etl_hits']
z_etl_hits0 = events0mm['gp_z_etl_hits']

theta_etl_hits100 = events100mm['gp_theta_etl_hits']
eta_etl_hits100 = events100mm['gp_eta_etl_hits']
phi_etl_hits100 = events100mm['gp_phi_etl_hits']
time_etl_hits100 = events100mm['gp_time_etl_hits']
energy_etl_hits100 = events100mm['gp_energy_etl_hits']
x_etl_hits100 = events100mm['gp_x_etl_hits']
y_etl_hits100 = events100mm['gp_y_etl_hits']
z_etl_hits100 = events100mm['gp_z_etl_hits']

theta_etl_hits = events['gp_theta_etl_hits']
eta_etl_hits = events['gp_eta_etl_hits']
phi_etl_hits = events['gp_phi_etl_hits']
time_etl_hits = events['gp_time_etl_hits']
energy_etl_hits = events['gp_energy_etl_hits']
x_etl_hits = events['gp_x_etl_hits']
y_etl_hits = events['gp_y_etl_hits']
z_etl_hits = events['gp_z_etl_hits']

#get all btl hit info
# theta_btl_hits0 = events0mm['gp_theta_btl_hits']
# eta_btl_hits0 = events0mm['gp_eta_btl_hits']
# phi_btl_hits0 = events0mm['gp_phi_btl_hits']
# time_btl_hits0 = events0mm['gp_time_btl_hits']
# energy_btl_hits0 = events0mm['gp_energy_btl_hits']
# x_btl_hits0 = events0mm['gp_x_btl_hits']
# y_btl_hits0 = events0mm['gp_y_btl_hits']
# z_btl_hits0 = events0mm['gp_z_btl_hits']

# theta_btl_hits100 = events100mm['gp_theta_btl_hits']
# eta_btl_hits100 = events100mm['gp_eta_btl_hits']
# phi_btl_hits100 = events100mm['gp_phi_btl_hits']
# time_btl_hits100 = events100mm['gp_time_btl_hits']
# energy_btl_hits100 = events100mm['gp_energy_btl_hits']
# x_btl__hits100 = events100mm['gp_x_btl_hits']
# y_btl_hits100 = events100mm['gp_y_btl_hits']
# z_btl_hits100 = events100mm['gp_z_btl_hits']


#make fake 4 vectors :)

reco_photon_vec4100 = ak.zip({"pt": reco_photon_pt100,"eta": reco_photon_eta100,"phi": reco_photon_phi100,"mass": reco_photon_M100,},with_name="PtEtaPhiMLorentzVector",)

mtd_etl_vec4100 = ak.zip({"pt": np.zeros_like(phi_etl_hits100),"eta": eta_etl_hits100,"phi": phi_etl_hits100,"mass" :np.zeros_like(phi_etl_hits100),},with_name="PtEtaPhiMLorentzVector",)
mtd_etl_vec40 = ak.zip({"pt": np.zeros_like(phi_etl_hits0),"eta": eta_etl_hits0,"phi": phi_etl_hits0,"mass" :np.zeros_like(phi_etl_hits0),},with_name="PtEtaPhiMLorentzVector",)
mtd_etl_vec4 = ak.zip({"pt": np.zeros_like(phi_etl_hits),"eta": eta_etl_hits,"phi": phi_etl_hits,"mass" :np.zeros_like(phi_etl_hits),},with_name="PtEtaPhiMLorentzVector",)

def dR_adjust_matching(x,y,z,theta,time,energy, mtd_vec4, photon_vec4, dR_range):

    #main matching of photon and gen e
    mp_cart = ak.cartesian([mtd_vec4, photon_vec4]) #not nested, axis=1

    mt_cart = ak.cartesian([mtd_vec4,time]) #ALERT!! ALERT!! I BELIEVE THIS MATCHING IS WRONG!! 
    mth_cart = ak.cartesian([mtd_vec4,theta]) #HAVE TO THINK OF A BETTER APPROACH
    me_cart = ak.cartesian([mtd_vec4,energy]) #NEEDS TO BE A FOUR VECTOR TO MATCH CORRECTLY
    mx_cart = ak.cartesian([mtd_vec4,x]) #I WONDER WHAT OTHER MATCHING HAS GONE WRONG
    my_cart = ak.cartesian([mtd_vec4,y])
    mz_cart = ak.cartesian([mtd_vec4,z])
    
    mean_photon_times = []
    for dR in dR_range:
        #Create a mask, True if less than 0.4 and True if more
        dRmask = np.absolute(delta_r(mp_cart['0'], mp_cart['1'])) < dR 

        #applying the mask, same dims as the combo but False just removes the ones w <0.4 dR
        mch_time = (mt_cart[dRmask])['1'] #get the time matched (from mask) info
        mch_theta = (mth_cart[dRmask])['1'] 
        mch_energy = (me_cart[dRmask])['1'] 
        mch_x = (mx_cart[dRmask])['1'] 
        mch_y = (my_cart[dRmask])['1'] 
        mch_z = (mz_cart[dRmask])['1'] 

        tof = (np.sqrt(mch_x**2 + mch_y**2 + mch_z**2)/10)*1/2.9979
        weightedTimeCell = ak.sum((mch_time-tof)*mch_energy*np.sin(mch_theta), axis=-1)
        totalEmEnergyCell = ak.sum(mch_energy*np.sin(mch_theta), axis=-1)

        adj_weightedTimeCell = ak.to_numpy(weightedTimeCell)/ak.to_numpy(totalEmEnergyCell)
        adj_weightedTimeCell[totalEmEnergyCell==0] = weightedTimeCell[totalEmEnergyCell==0]

        #res = ak.mean(ak.concatenate([weightedTimeCell[totalEmEnergyCell>0]/totalEmEnergyCell[totalEmEnergyCell>0], weightedTimeCell[totalEmEnergyCell==0]], axis=0), axis=0)

        mean_photon_times.append(np.mean(adj_weightedTimeCell))

    return mean_photon_times

dR_range = np.arange(0,1,0.001)
#mean_photons100 = dR_adjust_matching(x_etl_hits100,y_etl_hits100,z_etl_hits100,theta_etl_hits100,time_etl_hits100,energy_etl_hits100, mtd_etl_vec4100,reco_photon_vec4100, dR_range)
mean_photons0 = dR_adjust_matching(x_etl_hits0,y_etl_hits0,z_etl_hits0,theta_etl_hits0,time_etl_hits0,energy_etl_hits0, mtd_etl_vec40,reco_photon_vec40, dR_range)
mean_photons = dR_adjust_matching(x_etl_hits,y_etl_hits,z_etl_hits,theta_etl_hits,time_etl_hits,energy_etl_hits, mtd_etl_vec4,reco_photon_vec4, dR_range)


fig, ax = plt.subplots(figsize=(8, 8))

plt.title(r'Noise correlation $h\to XX\to 4e$: dR vs Photon Time', fontsize = 18)
plt.scatter(dR_range,mean_photons,c='red',s=3)
plt.scatter(dR_range,mean_photons0,c='blue',s=3)

plt.ylabel(r'Mean Photon Time (ns)',fontsize=18)
plt.xlabel('dR', fontsize=18)

plt.legend([r"$c\tau$=1000mm " , r"$c\tau$=0mm "], ncol = 2, loc="lower right",markerscale=5,frameon=True,fancybox=True)

finalizePlotDir('/home/users/hswanson13/public_html/MTD_timing_hists/')
fig.savefig('/home/users/hswanson13/public_html/MTD_timing_hists/dR_noise_correlation.png')