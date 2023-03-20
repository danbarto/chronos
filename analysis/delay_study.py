#!/usr/bin/env python3

# from here https://github.com/hswanson13/chronos/blob/main/analysis/timing_plots/MTD_timing_hists/matched_reco_photons_time.py
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

import hist

from Tools.helpers import get_four_vec_fromPtEtaPhiM, delta_phi, cross, delta_r, delta_r2, choose, match, finalizePlotDir

if __name__ == '__main__':
    c = 29.9792458

#    # these are all just 200 events.
#    events0mm = NanoEventsFactory.from_root(
#        '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing0mm.root',
#        schemaclass = BaseSchema,
#        treepath='demo/tree',
#        entry_stop = 1000).events()
#
#    events100mm = NanoEventsFactory.from_root(
#        '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
#        schemaclass = BaseSchema,
#        treepath='demo/tree',
#        entry_stop = 1000).events()


    events1000mm = NanoEventsFactory.from_root(
#        '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing1000mm.root',
        #'/home/users/dspitzba/timing/CMSSW_11_3_1_patch1/src/Phase2Timing/ntuple_phase2timing1000mm.root',
        #'/home/users/dspitzba/timing/CMSSW_11_3_1_patch1/src/Phase2Timing/output.root',
        '/home/users/dspitzba/timing/CMSSW_11_3_1_patch1/src/Phase2Timing/test_pv_1000mm_10k.root',
        schemaclass = BaseSchema,
        treepath='demo/tree',
        entry_stop = 1000).events()

    gen_ele = ak.zip({
        'pt': events1000mm['e_pt'],
        'eta': events1000mm['e_eta'],
        'phi': events1000mm['e_phi'],
        'time': (events1000mm['e_ebdelay']*(abs(events1000mm['e_eta'])<1.48) + events1000mm['e_hgdelay']*(abs(events1000mm['e_eta'])>1.48))*10**9,
        'ctau': events1000mm['e_ctau']/10,  # I guess this is cm then??
        'mass': np.zeros_like(events1000mm['e_pt']),
        }, with_name="PtEtaPhiMLorentzVector")

    reco_photon = ak.zip({
        'pt': events1000mm['reco_photon_pt'],
        'eta': events1000mm['reco_photon_eta'],
        'phi': events1000mm['reco_photon_phi'],
        'time': events1000mm['reco_photon_MTDtime'],  # this does not take into account the PV time!
        'mass': np.zeros_like(events1000mm['reco_photon_pt']),
        }, with_name="PtEtaPhiMLorentzVector")

    etl_hits = ak.zip({
        'x': events1000mm['gp_x_etl_hits'],
        'y': events1000mm['gp_y_etl_hits'],
        'z': events1000mm['gp_z_etl_hits'],
        'eta': events1000mm['gp_eta_etl_hits'],
        'time': events1000mm['gp_time_etl_hits'],
        'energy': events1000mm['gp_energy_etl_hits'],
    }, with_name='ThreeVector')  # checked against gp_phi_etl_hits, gp_theta_etl_hits and agrees

    btl_hits = ak.zip({
        'x': events1000mm['gp_x_btl_hits'],
        'y': events1000mm['gp_y_btl_hits'],
        'z': events1000mm['gp_z_btl_hits'],
        'eta': events1000mm['gp_eta_btl_hits'],
        'time': events1000mm['gp_time_btl_hits'],
        'energy': events1000mm['gp_energy_btl_hits'],
    }, with_name='ThreeVector')  # checked against gp_phi_btl_hits, gp_theta_btl_hits and agrees

    pv = ak.zip({
        'x': events1000mm['pv_x'],
        'y': events1000mm['pv_y'],
        'z': events1000mm['pv_z'],
        'time': events1000mm['pv_t'],
    }, with_name='ThreeVector')

    #gen_pv = ak.zip({
    #    'x': events1000mm['gen_pv_x'],
    #    'y': events1000mm['gen_pv_y'],
    #    'z': events1000mm['gen_pv_z'],
    #    'time': events1000mm['gen_pv_t'],
    #}, with_name='ThreeVector')

    lead_pv = ak.flatten(pv[:,:1])

    mtd_hits = ak.concatenate([etl_hits, btl_hits], axis=1)
    mtd_hits['sl'] = ((mtd_hits.x - lead_pv.x)**2+(mtd_hits.y-lead_pv.y)**2+(mtd_hits.z-lead_pv.z)**2)**0.5  # straight line distance in cm
    mtd_hits['delay'] = (mtd_hits.time - lead_pv.time) - mtd_hits.sl/c
    mtd_hits['sl_no_pv'] = ((mtd_hits.x)**2+(mtd_hits.y)**2+(mtd_hits.z)**2)**0.5  # straight line distance in cm
    mtd_hits['delay_no_pv'] = (mtd_hits.time) - mtd_hits.sl_no_pv/c

    # find the closest MTD hit with
    # reco_photon.nearest(mtd_hits)
    # if necessary

    deltaR = 0.1
    matched_photon = reco_photon[match(reco_photon, gen_ele, deltaRCut=0.1)]
    #matched_mtd = mtd_hits[match(mtd_hits, matched_photon, deltaRCut=deltaR)]

    combs_pho_hit = ak.cartesian([matched_photon, mtd_hits], nested=True)
    combs_pho_gen = ak.cartesian([matched_photon, gen_ele], nested=True)
    matched_mtd_to_photon = combs_pho_hit[delta_r(combs_pho_hit['0'], combs_pho_hit['1'])<deltaR]
    matched_gen_to_photon = combs_pho_gen[delta_r(combs_pho_gen['0'], combs_pho_gen['1'])<0.1]

    # the below calculation is verified against the CMSSW plugin when NOT using the PV correction
    matched_photon['time_recalc'] = ak.sum(matched_mtd_to_photon['1'].delay*matched_mtd_to_photon['1'].energy*np.sin(matched_mtd_to_photon['1'].theta), axis=2) / ak.sum(matched_mtd_to_photon['1'].energy*np.sin(matched_mtd_to_photon['1'].theta), axis=2)
    matched_photon['time_recalc_no_pv'] = ak.sum(matched_mtd_to_photon['1'].delay_no_pv*matched_mtd_to_photon['1'].energy*np.sin(matched_mtd_to_photon['1'].theta), axis=2) / ak.sum(matched_mtd_to_photon['1'].energy*np.sin(matched_mtd_to_photon['1'].theta), axis=2)
    matched_photon['time_gen'] = ak.min(matched_gen_to_photon['1'].time, axis=2)

    time_res_no_pv = ak.flatten(matched_photon.time_gen - ak.nan_to_num(matched_photon.time_recalc_no_pv,0))
    time_res_no_pv = time_res_no_pv[time_res_no_pv<1000]  # filter out events with weird gen time

    time_res = ak.flatten(matched_photon.time_gen - ak.nan_to_num(matched_photon.time_recalc,0))
    time_res = time_res[time_res<1000]  # filter out events with weird gen time

    res_axis = hist.axis.Regular(19, -1.9, 1.9, name="time", label=r"time (ns)")
    time_res_h = hist.Hist(res_axis)
    time_res_h.fill(time_res)

    time_res_no_pv_h = hist.Hist(res_axis)
    time_res_no_pv_h.fill(time_res_no_pv)

    fig, ax = plt.subplots(figsize=(8, 8))
    time_res_h.plot1d(
            histtype="errorbar",
            ax=ax,
            label='PV corr',
            color='blue',
        )

    time_res_no_pv_h.plot1d(
            histtype="errorbar",
            ax=ax,
            label='no PV corr',
            color='red',
        )

    plt.legend(loc=0)
    plot_dir = '/home/users/dspitzba/public_html/MTD_timing_hists/'

    hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)
    fig.savefig(f'{plot_dir}/time_resolution.png')

    time_axis = hist.axis.Regular(20, 0.0, 10, name="time", label=r"time (ns)")
    ctau_axis = hist.axis.Regular(20, 0.0, 250, name="ctau", label=r"$c\tau$ (cm)")

    time_hist = hist.Hist(time_axis)
    time_hist.fill(ak.flatten(gen_ele.time, axis=1))

    fig, ax = plt.subplots(figsize=(8, 8))
    hep.histplot([time_hist.values()],
            time_hist.axes[0].edges,
            histtype="step",
            stack=False,
            #label=[fr'$h\to XX\to 4e$: {name}' for name in names],
            #color=colors,
            ax=ax,)

    hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

    #ax.set_xlabel(r'$\varphi$')
    #plt.xlim([-3.2, 3.2])
    #plt.ylim([-3.2, 3.2])
    #ax.set_ylabel(r'$\eta$')

    plt.legend(loc=0)

    finalizePlotDir(plot_dir)
    fig.savefig(f'{plot_dir}/delay.png')

    ctau_hist = hist.Hist(ctau_axis)
    ctau_hist.fill(ak.flatten(gen_ele.ctau, axis=1))

    fig, ax = plt.subplots(figsize=(8, 8))
    hep.histplot([ctau_hist.values()],
            ctau_hist.axes[0].edges,
            histtype="step",
            stack=False,
            #label=[fr'$h\to XX\to 4e$: {name}' for name in names],
            #color=colors,
            ax=ax,)

    hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

    #ax.set_xlabel(r'$\varphi$')
    #plt.xlim([-3.2, 3.2])
    #plt.ylim([-3.2, 3.2])
    #ax.set_ylabel(r'$\eta$')

    plt.legend(loc=0)

    plot_dir = '/home/users/dspitzba/public_html/MTD_timing_hists/'
    finalizePlotDir(plot_dir)
    fig.savefig(f'{plot_dir}/ctau.png')
    raise

    for i in range(len(events1000mm)):
        fig, ax = plt.subplots(figsize=(8, 8))

        x1, y1 = [-3.2, 3.2], [-1.6, -1.6]
        x2, y2 = [-3.2, 3.2], [1.6, 1.6]
        plt.plot(x1, y1, x2, y2, marker = '', linestyle='--', color='gray')

        plt.scatter(
            gen_ele.phi[i],
            gen_ele.eta[i],
            marker="2",
            color='gray',
            #c=gen_ele.time[0],
        )
        for el in gen_ele[i]:
            ax.annotate('{:.2f}ns'.format(el.time), (el.phi+0.1, el.eta-0.06), fontsize=10)
        for el in gen_ele[i]:
            ax.annotate('{:.0f}cm'.format(el.ctau), (el.phi+0.1, el.eta+0.06), fontsize=10)


        plt.scatter(
            mtd_hits.phi[i],
            mtd_hits.eta[i],
            c=mtd_hits.time[i] - mtd_hits.sl[i]/c,
            vmin=0, vmax=5,
        )
        cbar = plt.colorbar(ax=ax)
        cbar.set_label('MTD hit delay (ns)')

        plt.scatter(
            reco_photon.phi[i],
            reco_photon.eta[i],
            facecolors='none',
            edgecolor='black',
            s=8**2*np.pi,  # this is roughly r=0.1
            linewidth=2,
            #c=gen_ele.time[0],
        )
        for ph in reco_photon[i]:
            ax.annotate('{:.2f}'.format(ph.time), (ph.phi-0.2, ph.eta+0.15), fontsize=10)

        #hep.histplot([hist.counts() for hist in histograms],
        #        binning,
        #        histtype="step",
        #        stack=False,
        #        label=[fr'$h\to XX\to 4e$: {name}' for name in names],
        #        color=colors,
        #        ax=ax,)

        hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

        ax.set_xlabel(r'$\varphi$')
        plt.xlim([-3.2, 3.2])
        plt.ylim([-3.2, 3.2])
        ax.set_ylabel(r'$\eta$')


        plt.legend(loc=0)

        plot_dir = '/home/users/dspitzba/public_html/MTD_timing_hists/event_level/'
        finalizePlotDir(plot_dir)
        fig.savefig(f'{plot_dir}/event_{i}.png')

        plt.close()
