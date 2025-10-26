#!/usr/bin/python
from poetry import cu_gala as gala
from poetry import _options
 
 
filename = 'npc.xml'
build_method = gala.XMLReader(filename)
perform_config = gala.PerformConfig(_options.gpu)
all_info = gala.AllInfo(build_method,perform_config)
 
dt = 0.002
app = gala.Application(all_info, dt)

neighbor_list = gala.NeighborList(all_info, 2.0**(1.0/6.0)+1.6, 0.25)#(,rcut,rbuffer)

pf = gala.PairForce(all_info, neighbor_list)
pf.setParams('G', 'G',    1.0,  0.95, 1.0,  2.0**(1.0/6.0)+1.6,  gala.PairFunc.lj12_6)#(,,alpha, 0.0, 0.0, rcut)
app.add(pf)

bh = gala.BondForceHarmonic(all_info)
bh.setParams('G-G', 1000.0, 0.95)
app.add(bh)


id1= 1689
id2= 2342
np=2500

vu=[]
for i in range(0, id1):
	vu.append(i)
for i in range(id1+1, id2):
	vu.append(i)
for i in range(id2+1, np):
	vu.append(i)

group = gala.ParticleSet(all_info, vu)
comp_info = gala.ComputeInfo(all_info, group)

T = 1.1
bd = gala.LangevinNVT(all_info, group, T, 12345)
app.add(bd)

v = gala.VariantLinear()
v.setPoint(0, 40) # timesteps, temperature length
v.setPoint(10000000, 80)

groupa = gala.ParticleSet(all_info, "all")
axs = gala.AxialStretching(all_info, groupa)
axs.setBoxLength(v, 'Z')
axs.setPeriod(100)
app.add(axs)


sort_method = gala.Sort(all_info)
sort_method.setPeriod(400)
app.add(sort_method)

ZeroMomentum = gala.ZeroMomentum(all_info)
ZeroMomentum.setPeriod(100000)# (period)
app.add(ZeroMomentum)
 
DInfo = gala.DumpInfo(all_info, comp_info, 'data.log')
DInfo.setPeriod(400)
DInfo.dumpPressTensor()
DInfo.dumpBoxSize()
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
app.run(10000000)#(How many steps to run)