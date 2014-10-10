import networkx as nx
from units import *

# SYSTEMS
class System(nx.DiGraph):
	def cycle(self):
		nodes = self.nodes()
		for n in nodes:
			print 'Serial: ' + n.serial + '\nLabel: ' + n.label + ' \nProduced: ' + str(n.__class__.produced)
			#print type(n)
			#print nx.node_connected_component(self, n)

# DEVICE TYPES
class PowerRegulator(Device):
	code = 'PRG'
	produced = 0
	def __init__(self, label = '[Power Regulator]'):
		super(PowerRegulator, self).__init__(label)
		PowerRegulator.produced += 1
	
class Computer(Device):
	code = 'CMP'
	produced = 0
	def __init__(self, label = '[Computer]'):
		super(Computer, self).__init__(label)
		Computer.produced += 1

# CONNECTOR TYPES
class Switch(Connector):
	code = 'SWT'
	produced = 0
	def __init__(self, label = '[Switch]'):
		super(Switch, self).__init__(label)
		Switch.produced += 1

class Bus(Connector):
	code = 'BUS'
	produced = 0
	def __init__(self, label = '[bus]'):
		super(Bus, self).__init__(label)
		Bus.produced += 1

class Breaker(Connector):
	code = 'BRK'
	produced = 0
	def __init__(self, label = '[breaker]'):
		super(Breaker, self).__init__(label)
		Breaker.produced += 1
		
# SWITCH TYPES
class CircuitSelectorSwitch(Switch):
	label = '[Circuit Selector Switch]'

# GENERATOR TYPES
class PowerGenerator(Generator):
	label = '[Power generator]'
	
class SolarPanelArray(Generator):
	label = '[Solar panel array]'
	

			
		
class ElectricalSystem(System):
	label = 'Electrical System'
	
class DataSystem(System):
	label = 'Data System'
	
class LifeSupportSystem(System):
	label = 'Life Support System'
	
class HydraulicSystem(System):
	label = 'Hydraulic System'

# ELECTRICAL SYSTEM		

	
class Battery(ElectricalChargeContainer):
	code = 'BAT'
	produced = 0
	def __init__(self, hour, ampere, peukert = 1.2, label = '[battery]'):
		super(Battery, self).__init__(hour, ampere, peukert, label)
		Battery.produced += 1

class PowerSupplyBus(Bus):
	label = '[Power Supply Bus]'
	
# DATA SYSTEM

class DataBus(Bus):
	label = '[Data Bus]'
	
# LIFE SUPPORT SYSTEM
class OxygenTank(PressureContainer):
	label = '[Oxygen Tank]'
	




