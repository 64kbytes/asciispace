import random

#curl http://deron.meranda.us/data/census-dist-female-first.txt | \ awk '{print $1}'

# WORDS
class Words(object):
	
	Noun, Adjective, Verb, Adverb, MaleName, FemaleName, Surname = range(7)
	
	nouns = adjectives = verbs = adverbs = maleNames = fenaleNames = surnames = None
	
	@staticmethod
	def init():
		Words.load_nouns()
		Words.load_adjectives()
		Words.load_verbs()
		Words.load_adverbs()
		Words.load_names()
		
	@staticmethod
	def load_nouns():
		with open('gm/text/nouns.txt', 'r') as n:
			Words.nouns = n.readlines()
	@staticmethod		
	def load_adjectives():
		with open('gm/text/adjectives/2syllableadjectives.txt') as a:
			Words.adjectives = a.readlines()
	@staticmethod		
	def load_verbs():
		with open('gm/text/verbs/1syllableverbs.txt') as a:
			Words.verbs = a.readlines()
	@staticmethod	
	def load_adverbs():
		with open('gm/text/adverbs/1syllableadverbs.txt') as a:
			Words.adverbs = a.readlines()
	@staticmethod		
	def load_names():
		with open('gm/text/names/names_male.txt') as a:
			Words.maleNames = a.readlines()
		with open('gm/text/names/names_female.txt') as a:
			Words.femaleNames = a.readlines()
		with open('gm/text/names/surnames.txt') as a:
			Words.surnames = a.readlines()
	@staticmethod		
	def random(t):
		return {
	        Words.Noun: Words.nouns[random.randint(0, len(Words.nouns) - 1)].rstrip(),
	        Words.Adverb: Words.adverbs[random.randint(0, len(Words.adverbs) - 1)].rstrip(),
	        Words.Adjective: Words.adjectives[random.randint(0, len(Words.adjectives) - 1)].rstrip(),
	        Words.MaleName:	Words.maleNames[random.randint(0, len(Words.maleNames) - 1)].rstrip(),
	        Words.FemaleName: Words.femaleNames[random.randint(0, len(Words.maleNames) - 1)].rstrip(),
	        Words.Surname: Words.surnames[random.randint(0, len(Words.surnames) - 1)].rstrip()
        }.get(t, None)  
            
	@staticmethod
	def randomName(sex = None):
		if sex is None:
			sex = random.randint(0, 1)
			
		if sex == 1:
			name = Words.random(Words.MaleName).capitalize()
		else:
			name = Words.random(Words.FemaleName).capitalize()
			
		return ' '.join([name, Words.random(Words.Surname).capitalize()])
			
	@staticmethod
	def randomSpacecraftName():
		return {
			0: Words.random(Words.Noun).capitalize(),
			1: Words.random(Words.Adjective).capitalize(),
			2: ' '.join([Words.random(Words.Adjective).capitalize(), Words.random(Words.Noun).capitalize()]),
			3: ' '.join([Words.random(Words.Adjective).capitalize(), Words.random(Words.FemaleName).capitalize()]),
			4: ' '.join([Words.random(Words.Adjective).capitalize(), Words.random(Words.MaleName).capitalize()])
		}[random.randint(0, 4)]
		
		
		
		
		
		
