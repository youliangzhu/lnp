#!/usr/bin/python
from poetry import cu_gala as gala
from poetry import _options
 
 
filename = 'tran.xml'
build_method = gala.XMLReader(filename)
perform_config = gala.PerformConfig(_options.gpu)
all_info = gala.AllInfo(build_method,perform_config)
 
dt = 0.002
app = gala.Application(all_info, dt)

neighbor_list = gala.NeighborList(all_info, 2.0**(1.0/6.0)+1.6, 0.25)#(,rcut,rbuffer)

pf = gala.PairForce(all_info, neighbor_list)
pf.setParams('Hn', 'Hn',   1.0,  0.95, 1.0,  0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Tn', 'Tn',   1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T1n', 'T1n', 1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Hn', 'Tn',   1.0,  0.95, 1.0,  0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Hn', 'T1n',  1.0,  0.95, 1.0,  0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Tn', 'T1n',  1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('G', 'Hn',   1.5,  1.0, 1.0,   2.0**(1.0/6.0)+1.6, gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
#pf.setParams('G', 'Hn',   1.0,  1.0, 1.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'Tn',   1.0,  0.95, 1.0,  0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'T1n',  1.0,  0.95, 1.0,  0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'G',    1.0,  1.0, 1.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('W', 'W',    0.0,  1.0, 1.0,  2.0**(1.0/6.0),  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('W', 'Hn',   1.0,  1.0, 1.0,  2.0**(1.0/6.0),  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('W', 'Tn',   1.0,  1.0, 1.0,  2.0**(1.0/6.0),  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('W', 'T1n',  1.0,  1.0, 1.0,  2.0**(1.0/6.0),  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('W', 'G',    1.0,  1.0, 1.0,  2.0**(1.0/6.0),  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
app.add(pf)

bh = gala.BondForceHarmonic(all_info)
bh.setParams('Hn-T1n', 10.0, 4.0)
bh.setParams('Hn-Tn',  1000.0, 0.95)
bh.setParams('Tn-T1n', 1000.0, 0.95)
bh.setParams('G-G', 1000.0, 0.95)
app.add(bh)


group = gala.ParticleSet(all_info, ["Hn", "Tn", "T1n", "G"])
comp_info = gala.ComputeInfo(all_info, group)

T = 1.1
bd = gala.LangevinNVT(all_info, group, T, 12345)
app.add(bd)

v = gala.VariantLinear()
v.setPoint(0, 0.0) # time step, box length.
v.setPoint(100000, 0.0)
v.setPoint(1000000, -0.015)

axs = gala.ExternalForce(all_info, group)
axs.setForce(v, "Z")
app.add(axs)

ljw=gala.LJWallForce(all_info, 1.0*2.0**(1.0/6.0))
ljw.setBoundaryDirection(False, False, True)
ljw.setParams('Hn',  1.0, 1.0, 1.0)
ljw.setParams('Tn',  1.0, 1.0, 1.0)
ljw.setParams('T1n', 1.0, 1.0, 1.0)
ljw.setParams('G',   1.0, 1.0, 1.0)
app.add(ljw)

sort_method = gala.Sort(all_info)
sort_method.setPeriod(400)
app.add(sort_method)

ZeroMomentum = gala.ZeroMomentum(all_info)
ZeroMomentum.setPeriod(100000)# (period)
app.add(ZeroMomentum)
 
DInfo = gala.DumpInfo(all_info, comp_info, 'data.log')
DInfo.setPeriod(400)
app.add(DInfo)
 
mol2 = gala.MOL2Dump(all_info, 'particles')
mol2.setPeriod(0)# (period)
app.add(mol2)
 
dcd = gala.DCDDump(all_info, 'particles',True)
dcd.setPeriod(100000)# (period)
app.add(dcd)
 
xml = gala.XMLDump(all_info, 'particles')
xml.setPeriod(20000)# (period)
xml.setOutputBond(True)
xml.setOutputVelocity(True)
xml.setOutputMass(True)
app.add(xml)


#ready ro run

app.run(  100000)#(How many steps to run)
app.setDt(0.005)
app.run(  10000000)#(How many steps to run)
