
exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

events = NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing0mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()

pt = events['e_pt']
eta = events['e_eta']
phi = events['e_phi']
m = np.zeros_like(pt)
vec4 = ak.zip( #vec4 this will get the four vector of whatever you give it
    {
        "pt": pt,
        "eta": eta,
        "phi": phi,
        "mass": m,
    },
    with_name="PtEtaPhiMLorentzVector",
)


inv_mass = (vec4[:,0] + vec4[:,1]).mass

bin_start = 0
bin_end = 100
n_bins = 10
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=0mm'
color='b'

arr = inv_mass
xlabel = 'Invarient Mass of Gen Ele'
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

fig.savefig('/home/users/hswanson13/public_html/invarient_mass/inv_mass_gen_e.png')
