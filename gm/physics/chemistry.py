# CHEMISTRY
class ChemicalElement:
	def __init__(self, atomicWeight):
		self.atomicWeight = atomicWeight
	
	def mol(self, gram):
		return gram / self.atomicWeight
		
	def gram(self, mol):
		return self.atomicWeight * mol
		

OXYGEN		= ChemicalElement(15.9999)
NITROGEN	= ChemicalElement(14.007)
IDEAL_GAS_CONST = 0.08205746 # atm L / mol K