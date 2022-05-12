#!/usr/bin/env python3

from RootTools.core.standard import *
from yahist import Hist1D


test = FWLiteSample.fromFiles("test", files = ['file:./output_1.root'])

products = {
    'jets':{'type':'vector<pat::Jet>', 'label': ( "slimmedJets" )},
    'mets':{'type':'vector<pat::MET>',  'label':( "slimmedMETs" )},
    'rho': {'type':'double', 'label': ("fixedGridRhoFastjetAll")},
    'pf':  {'type':'vector<pat::PackedCandidate>', 'label': ("packedPFCandidates")},
    'ele': {'type':'vector<pat::Electron>', 'label':("slimmedElectrons")},
    'mu':  {'type':'vector<pat::Muon>', 'label':("slimmedMuons")},
    'pho': {'type':'vector<pat::Photon>', 'label':("slimmedPhotons")},
    'tau': {'type':'vector<pat::Tau>', 'label':("slimmedTaus")},
    'tracksMTD': {'type':'vector<reco::Track>', 'label':("trackExtenderWithMTD")},
    'tracks': {'type':'vector<reco::Track>', 'label':("generalTracks")},
   }


r = test.fwliteReader( products = products )

r.start()

dt_MTD = Hist1D(bins="100,0,5")

while r.run():

    #for muon in r.event.mu:
    #    # get muon time with muon.time().timeAtIpInOut or muon.time().timeAtIpOutIn
    #    # this seems to be old though
    #    #print (muon.pt(), muon.eta(), muon.time().timeAtIpInOut, muon.time().timeAtIpOutIn)
    #    pass

    print (len(r.event.tracks), len(r.event.tracksMTD))

    tmp = []
    for track in r.event.tracksMTD:
        if track.t0()>0:
            tmp.append(track.t0())

    dt_MTD.fill(tmp)

    #break

import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)

fig, ax = plt.subplots(1,1, figsize=(10,10))

hep.cms.label(
    "Preliminary",
    data=False,
    lumi=3000,
    #com=14,
    loc=0,
    ax=ax,
)

hep.histplot(
    [dt_MTD.counts],
    dt_MTD.edges,
    histtype="fill",
    stack=False,
    label=['test'],
    color=['#1982c4'],
    ax=ax)


ax.set_yscale('log')
fig.savefig('/home/users/dspitzba/public_html/dt_log.png')

ax.set_yscale('linear')
fig.savefig('/home/users/dspitzba/public_html/dt_lin.png')
