import physics.chemistry as ch

class Unit(object):
	code = 'U'
	produced = 0
	def __init__(self, label = ''):
		serialPart = self.__class__.code + str(self.__class__.produced)
		self.serial = "{0}{1}{2}".format(Unit.code, Unit.produced, serialPart)
		self.label = label
		Unit.produced += 1
		
	def __str__(self):
		return self.serial
	
class Device(Unit):
	code = 'D'
	produced = 0
	def __init__(self, label = ''):
		super(Device, self).__init__(label)
		Device.produced += 1

class Generator(Unit):
	code = 'G'
	produced = 0
	def __init__(self, label = ''):
		super(Generator, self).__init__(label)
		Generator.produced += 1

class Connector(Unit):
	code = 'C'
	produced = 0
	def __init__(self, label = ''):
		super(Connector, self).__init__(label)
		Connector.produced += 1

class PhysicalStorage(Unit):
	code = 'PS'
	produced = 0
	def __init__(self, label = ''):
		super(PhysicalStorage, self).__init__(label)
		PhysicalStorage.produced += 1

class PressureContainer(Unit):
	code = 'PC'
	produced = 0
	def __init__(self, volume, temperature, mass = 0, label = ''):
		self.volume = volume
		self.temperature = temperature
		self.pressure = (mass * ch.IDEAL_GAS_CONST * temperature) / volume
		super(PressureContainer, self).__init__(label)

class ElectricalChargeContainer(Unit):
	code = 'EC'
	produced = 0
	def __init__(self, hour, ampere, peukert = 1.2, label = ''):
		self.peukert = peukert
		self.charge = hour * ampere
		super(ElectricalChargeContainer, self).__init__(label)