
exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

events= NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()


l_list = [2,3,4,5,6]
def get_diphoton_mass(l):
        four_photon_pt = ak.Array([i for i in events['reco_photon_pt'] if len(i)==l]) 
        four_photon_eta = ak.Array([i for i in events['reco_photon_eta'] if len(i)==l])        
        four_photon_phi = ak.Array([i for i in events['reco_photon_phi'] if len(i)==l])
        four_photon_M = np.zeros_like(four_photon_pt)

        RP_vec4 = ak.zip( #vec4 this will get the four vector of whatever you give it
            {
                "pt": four_photon_pt,
                "eta": four_photon_eta,
                "phi": four_photon_phi,
                "mass": four_photon_M,
            },
            with_name="PtEtaPhiMLorentzVector",
        )

        i_array = ak.Array(range(l)) #l is 4
        indices = ak.to_list(ak.combinations(i_array, 2, axis=0))
        diphoton_mass = ak.flatten([(RP_vec4[:,pair[0]]+RP_vec4[:,pair[1]]).mass for pair in indices])
        return diphoton_mass

all_diphoton_mass = []
for l in l_list:
        all_diphoton_mass += list(get_diphoton_mass(l))


bin_start = 0
bin_end = 150
n_bins = 20
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=100mm'
color='b'

arr = np.clip(all_diphoton_mass,bin_start,bin_end-1)
xlabel = 'Invarient Mass of All Reco Photons (GeV)'
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

fig.savefig('/home/users/hswanson13/public_html/invarient_mass/inv_mass_all_reco_photons.png')