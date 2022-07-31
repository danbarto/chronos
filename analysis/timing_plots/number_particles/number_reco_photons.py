exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

events= NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()


n_reco_photon = ak.Array([len(i) for i in events['reco_photon_pt']])

bin_start = 0
bin_end = 10
n_bins = 11
bin_width = (bin_end - bin_start)/n_bins

name=fr'$c\tau$=100mm'
color='b'

arr = np.clip(n_reco_photon,bin_start,bin_end-0.2)
xlabel = 'Number of Reco Photons'
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

fig.savefig('/home/users/hswanson13/public_html/number_particles/number_reco_photons.png')
#finalizePlotDir('/home/users/hswanson13/public_html/number_gen_e2.png')