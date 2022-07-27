#!/usr/bin/env python3

import awkward as ak
import numpy as np
import boost_histogram as bh

from coffea.nanoevents import NanoEventsFactory, BaseSchema
from Tools.helpers import get_four_vec_fromPtEtaPhiM, choose, cross, match, delta_r

# Load events

if __name__ == '__main__':

    events = NanoEventsFactory.from_root(
        '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing.root',
        schemaclass = BaseSchema,
        treepath='demo/tree',
        entry_stop = 1000).events()

    # get generated electrons
    gen_ele = get_four_vec_fromPtEtaPhiM(
        None,
        events['e_pt'],
        events['e_eta'],
        events['e_phi'],
        ak.zeros_like(events['e_phi']),
        copy=False,
    )

    # get reco track four vectors
    reco_track = get_four_vec_fromPtEtaPhiM(
        None,
        events['track_pt'],
        events['track_eta'],
        events['track_phi'],
        ak.zeros_like(events['track_phi']),
        copy=False,
    )

    # Some examples of what we can do:
    # all combinations of two electrons
    dielectron = choose(gen_ele, n=2)  # e.g. do dielectron.mass to get the invariant mass


    # all combinations of electrons and tracks
    track_ele = cross(gen_ele, reco_track)

    # get the delta r between any of these combinations
    track_ele_dR = delta_r(track_ele['0'], track_ele['1'])

    # find tracks that are matched to a gen electron
    matched_track = reco_track[match(reco_track, gen_ele, deltaRCut=0.2)]
