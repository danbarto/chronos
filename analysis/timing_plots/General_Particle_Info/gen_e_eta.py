exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

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


#get gen electron times for 0mm, 100mm, 1000mm
ge_eta = events['e_eta']

ge_eta100 = events100mm['e_eta']

ge_eta0 = events0mm['e_eta']



bin_start = -10
bin_end = 10
n_bins = 20
bin_width = (bin_end - bin_start)/n_bins


names = [r'$c\tau$=1000mm',r'$c\tau$=100mm',r'$c\tau$=0mm']
colors = ['b','r','g']

arrs = [ak.flatten(ge_eta),ak.flatten(ge_eta100),ak.flatten(ge_eta0)]
xlabel = r'Gen Ele $\eta$'
binning = np.linspace(bin_start,bin_end,n_bins)
histograms = []
for arr in arrs:
    hist = bh.Histogram(bh.axis.Variable(binning), storage=bh.storage.Weight(),)
    hist.fill(arr, weight=np.ones_like(arr),)
    area = sum(hist.counts()) #bin_width*hist.counts(), guess not! haha works
    histograms.append(hist)

fig, ax = plt.subplots(figsize=(8, 8))
hep.histplot([hist.counts() for hist in histograms],
        binning,
        histtype="step",
        stack=False,
        label=[fr'$h\to XX\to 4e$: {name}' for name in names],
        color=colors,
        ax=ax,)

hep.cms.label("Preliminary",data=False,lumi='X',com=14,loc=0,ax=ax,fontsize=15,)

ax.set_ylabel(r'Counts')
ax.set_xlabel(xlabel, fontsize=18)
plt.legend(loc=0)

fig.savefig('/home/users/hswanson13/public_html/General_Particle_Info/gen_e_eta.png')