
exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

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

# all combinations of electrons and tracks
track_ele = cross(gen_e_vec4, track_vec4)

# get the delta r between any of these combinations
track_ele_dR = delta_r(track_ele['0'], track_ele['1'])

#print(len(ak.flatten(track_ele_dR[track_ele_dR<0.4])))
all_track_ele = [] #ak_flatten above
for track in track_ele_dR:
    for dr in track:
        all_track_ele.append(dr)

#HISTOGRAM OF dR
dR420 = all_track_ele

bin_start = 0
bin_end = 10 
n_bins = 100
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=100mm'
color='b'

arr = np.clip(dR420,bin_start,bin_end-1)
xlabel = r'dR$^2$ = $\eta^2$ +  $\phi^2$ '
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

fig.savefig('/home/users/hswanson13/public_html/matching_tracks/dR_tracks.png')