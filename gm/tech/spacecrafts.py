from systems import *
from words import *

# SPACECRAFT	
class Spacecraft:
	
	def __init__(self):	 
	
		self.label = Words.randomSpacecraftName()
		self.sys = System()
		self.sys.label = self.label + ' system';

		# set empty electrical system
		self.electricalSystem = ElectricalSystem()		
		self.electricalSystem.name = 'Electrical System'
		
		# set empty data system
		self.dataSystem = DataSystem()
		self.dataSystem.name = 'Data System'
		
		# set empty life support system
		self.lifeSupportSystem = LifeSupportSystem()
		self.lifeSupportSystem.name = 'Life Support System'
			
		# set empty hydraulic system
		self.hydraulicSystem = HydraulicSystem()
		self.hydraulicSystem.name = 'Hydraulic System'
		
	@staticmethod
	def create():			
		ship = Spacecraft()	
		
		# electrical systen
		gen_A		= PowerGenerator('MAIN PWR')
		gen_B		= PowerGenerator('AUX PWR')
		brk_gen_A	= Breaker('CIRCUIT BREAKER[ main pwr ]')
		brk_gen_B	= Breaker('CIRCUIT BREAKER[ aux pwr ]')
		brk_gen_C	= Breaker('CIRCUIT BREAKER[ solar pwr ]')
		swt_A		= CircuitSelectorSwitch('SWITCH SELECTOR A')
		swt_B		= CircuitSelectorSwitch('SWITCH SELECTOR B')		
		sol			= SolarPanelArray('SOLAR PWR')
		reg			= PowerRegulator('PWR REGULATOR')
		pwr_bus		= PowerSupplyBus('PWR SUPPLY BUS')
		bat_A		= Battery(**{'hour': 24, 'ampere': 10, 'label': 'MAIN BATTERY'})
		bat_B		= Battery(**{'hour': 24, 'ampere': 10, 'label': 'AUX_BATTERY'})
		
		# data system
		com = Computer()
		dat_bus = DataBus()
		
		# life support system
		tnk = OxygenTank(5000, 90, ch.OXYGEN.mol(100000))
		
		
		ship.electricalSystem.add_nodes_from([gen_A, gen_B, brk_gen_A, brk_gen_B, swt_A, sol, reg, bat_A]);
		ship.electricalSystem.add_edges_from([(gen_A, brk_gen_A), (brk_gen_A, swt_A)])
		ship.electricalSystem.add_edges_from([(gen_B, brk_gen_B), (brk_gen_B, swt_A)]);
		ship.electricalSystem.add_edges_from([(sol, reg), (reg, bat_A), (bat_A, brk_gen_C), (brk_gen_C, swt_A)])
		ship.electricalSystem.add_edges_from([(swt_A, pwr_bus)])
		ship.electricalSystem.add_edges_from([(pwr_bus, com)])	
		
		ship.dataSystem.add_nodes_from([com, dat_bus, gen_A, gen_B, reg])
		ship.dataSystem.add_edges_from([(com, dat_bus), (dat_bus, gen_A), (dat_bus, gen_B), (dat_bus, reg)])

		return ship	
