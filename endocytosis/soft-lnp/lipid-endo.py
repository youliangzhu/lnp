#!/usr/bin/python
from poetry import cu_gala as gala
from poetry import _options
 
 
filename = 'endo.xml'
build_method = gala.XMLReader(filename)
perform_config = gala.PerformConfig(_options.gpu)
all_info = gala.AllInfo(build_method,perform_config)
 
dt = 0.002
app = gala.Application(all_info, dt)

neighbor_list = gala.NeighborList(all_info, 2.0**(1.0/6.0)+1.6, 0.25)#(,rcut,rbuffer)
                                        
neighbor_list.setRCutPair('H', 'H',     0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T', 'T',      2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('T1', 'T1',    2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('H', 'T',     0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('H', 'T1',    0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T', 'T1',     2.0**(1.0/6.0)+1.6)
                                       
neighbor_list.setRCutPair('Hn', 'Hn',   0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('Tn', 'Tn',    2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('T1n', 'T1n',  2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('Hn', 'Tn',   0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('Hn', 'T1n',  0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('Tn', 'T1n',   2.0**(1.0/6.0)+1.6)
                                       
neighbor_list.setRCutPair('H', 'Hn',     2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('H', 'Tn',    0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('H', 'T1n',   0.95*2.0**(1.0/6.0))
                                       
neighbor_list.setRCutPair('T', 'Hn',    0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T', 'Tn',    0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T', 'T1n',   0.95*2.0**(1.0/6.0))
                                       
neighbor_list.setRCutPair('T1', 'Hn',   0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T1', 'Tn',   0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('T1', 'T1n',  0.95*2.0**(1.0/6.0))
                                       
neighbor_list.setRCutPair('G', 'H',     0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('G', 'T',     0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('G', 'T1',    0.95*2.0**(1.0/6.0))
                                       
neighbor_list.setRCutPair('G', 'Hn',     2.0**(1.0/6.0)+1.6)
neighbor_list.setRCutPair('G', 'Tn',    0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('G', 'T1n',   0.95*2.0**(1.0/6.0))
neighbor_list.setRCutPair('G', 'G',      2.0**(1.0/6.0)+1.6)


pf = gala.PairForce(all_info, neighbor_list)
pf.setParams('H', 'H',     1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T', 'T',     1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T1', 'T1',   1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('H', 'T',     1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('H', 'T1',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T', 'T1',    1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('Hn', 'Hn',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Tn', 'Tn',   1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T1n', 'T1n', 1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Hn', 'Tn',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Hn', 'T1n',  1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('Tn', 'T1n',  1.0,  1.6,  0.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.cos_wc)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('H', 'Hn',    0.6,   1.0, 1.0,  2.0**(1.0/6.0)+1.6, gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('H', 'Tn',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('H', 'T1n',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('T', 'Hn',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T', 'Tn',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T', 'T1n',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('T1', 'Hn',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T1', 'Tn',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('T1', 'T1n',  1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('G', 'H',     1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'T',     1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'T1',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)

pf.setParams('G', 'Hn',    1.0,  1.0, 1.0,   2.0**(1.0/6.0)+1.6, gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'Tn',    1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'T1n',   1.0,  0.95, 1.0, 0.95*2.0**(1.0/6.0), gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
pf.setParams('G', 'G',     1.0,  1.0, 1.0,   2.0**(1.0/6.0)+1.6, gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
app.add(pf)

bh = gala.BondForceHarmonic(all_info)
bh.setParams('H-T1', 10.0, 4.0)
bh.setParams('H-T',  1000.0, 0.95)
bh.setParams('T-T1', 1000.0, 0.95)
bh.setParams('Hn-T1n', 10.0, 4.0)
bh.setParams('Hn-Tn',  1000.0, 0.95)
bh.setParams('Tn-T1n', 1000.0, 0.95)
bh.setParams('G-G', 1000.0, 0.95)
app.add(bh)


group = gala.ParticleSet(all_info, "all")
comp_info = gala.ComputeInfo(all_info, group)

T = 1.1
# build rigid NVE integration

bd = gala.LangevinNVT(all_info, group, T, 12345)
app.add(bd)

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
xml.setPeriod(100000)# (period)
xml.setOutputBond(True)
xml.setOutputVelocity(True)
xml.setOutputMass(True)
app.add(xml)

#ready ro run

app.run(  100000)#(How many steps to run)
app.setDt(0.005)
app.run(  50000000)#(How many steps to run)
