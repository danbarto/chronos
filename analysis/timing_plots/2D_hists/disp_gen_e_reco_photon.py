exec(open("/home/users/hswanson13/CMSSW_12_2_0/src/chronos/analysis/timing_plots/config_plots.py").read())

events= NanoEventsFactory.from_root(
    '/home/users/hswanson13/CMSSW_11_3_1_patch1/src/Phase2Timing/Phase2TimingAnalyzer/python/ntuple_phase2timing100mm.root',
    schemaclass = BaseSchema,
    treepath='demo/tree',
    entry_stop = 1000).events()

e_vx = events['e_vx']
e_vy = events['e_vy']
e_vz = events['e_vz']

e_R = np.sqrt(e_vx**2 + e_vy**2 + e_vz**2)
max_e_R = [max(i) for i in e_R]

n_reco_photon = ak.to_numpy(ak.Array([len(i) for i in events['reco_photon_pt']]))

fig, ax = plt.subplots(figsize=(8, 8))

plt.title(fr"CMS Preliminary: $c\tau$=100mm")
plt.hist2d(n_reco_photon, max_e_R, bins=(9,9))
plt.colorbar()
plt.xlabel('number of photons per event')
plt.ylabel('maximum LLP vertex displacement')

fig.savefig('/home/users/hswanson13/public_html/2Dhists/disp_gen_e_reco_photon.png')
#finalizePlotDir('/home/users/hswanson13/public_html/number_gen_e2.png')