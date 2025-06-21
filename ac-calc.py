from tabulate import tabulate

# check that var is a list of three numbers
def checklist(var):
  return (
      isinstance(var, list) and len(var) == 3 
      and (all(isinstance(x, (int, float)) for x in var)) 
      and not (all(isinstance(x, bool) for x in var))
      )

# coverage of a slot
basic_slots = {
	'head':	0.1,
	'body':	0.4,
	'arm':	0.08,
	'hand':	0.07,
	'leg':	0.06,
	'foot':	0.04,
	'test':	0
}

extended_slots_1 = {
	'jacket': 0.56,
	'pants': 0.12,
	'boots': 0.08
}

# materials of armor, their ideal ac and rigidity
# ЭТО ВРЕМЕННЫЕ ЗНАЧЕНИЯ ИЗ СТАРОЙ ВЕРСИИ ПРАВИЛ --- ИЗМЕНИТЬ!
basic_materials = {
	'cloth':	[[7,6,5],	0,	1],
	'leather-s':[[12,7,5],	0.2,1],
	'leather-h':[[15,12,7],	0.4,1],
	'gambeson':	[[9,5,10],	0.1,1],
	'mail':		[[19,10,5],	0.5,2],
	'scales':	[[19,17,13],0.7,2], # scales, lamellar, laminar
	'plate':	[[19,19,15],1,	3],
	'test':		[[0,0,0],	0,	1]
}

class armor_piece:

	def __init__(self,slot,material,S=0,slotsdict=basic_slots,materialsdict=basic_materials):
		"""
		Armor piece

		:param slot: 			Armor slot (basic: head, arm, hand, body, leg, foot). Test slot - 'test' (C=0)
		:param material: 		Armor material (basic: cloth, leather-s, leather-h, gambeson, mail, scales, plate). Test material - 'test' (I,R=0)
		:param S: 				Shape factor (applied only to plate, for other materials S=0)
		:param slotsdict:		Dict for custom slots ({'<slot_name>':<coverage>}). Default dict - basic_slots. 
		:param materialsdict:	Dict for custom materials ({'<material_name>':<[[<Is>,<Ip>,<Ib>],<R>]>}). 
								I - slashing, piercing, bludgeoning ac. R - rigidity. Default dict - basic_materials. 
		"""
		# slot and material names
		if str(slot) in slotsdict.keys():
			self.__slot = str(slot)
		else:
			print(f'No such slot: {slot}. Setting to test (C=0).')
			self.__slot = 'test'

		if str(material) in materialsdict.keys():
			self.__material = str(material)
		else:
			print(f'No such material: {material}. Setting to test (C=0).')
			self.__material = 'test'


		# ideal ac of armor type, I = [Slashing, Piercing, Bludgeoning]
		self.__ideal = materialsdict[self.__material][0]

		# rigidity of armor type (cloth = 0, plate = 1)
		self.__rigidity = materialsdict[self.__material][1]

		# armor grade
		self.__grade = materialsdict[self.__material][2]

		# coverage of armor slot
		self.__coverage = slotsdict[self.__slot]

		# shape factor, used only for plate
		if self.__material != 'plate':
			self.__shape = 0
		elif (isinstance(S, (int,float))) and (0 <= S <= 1):
			self.__shape = S
		else: 
			print(f'Wrong shape: {S}. Should be a number between 0 and 1. Setting to 0.')
			self.__shape = 0



	# block of setters and getters:
	@property
	def slot(self):
		return self.__slot

	@slot.setter
	def slot(self, name):
		self.__slot = str(name)

	@property
	def material(self):
		return self.__material

	@material.setter
	def slot(self, name):
		self.__material = str(name)

	@property
	def ideal(self):
		return self.__ideal

	@ideal.setter
	def ideal(self,I):
		self.__ideal = I if checklist(I) else print(f'Wrong ideal: {I}. Should be a list of three numbers.')

	@property
	def rigidity(self):
		return self.__rigidity

	@rigidity.setter
	def rigidity(self,R):
		self.__rigidity = R if (isinstance(R, (int,float))) and (0 <= R <= 1) else print(f'Wrong rigidity: {R}. Should be a number between 0 and 1.')

	@property
	def coverage(self):
		return self.__coverage

	@coverage.setter
	def coverage(self,C):
		self.__coverage = C if (isinstance(C, (int,float))) and (0 <= C <= 1) else print(f'Wrong coverage {C}. Should be a number between 0 and 1.')

	@property
	def shape(self):
		return self.__shape

	@shape.setter
	def coverage(self,S):
		self.__shape = S if (isinstance(S, (int,float))) and (0 <= S <= 1) else print(f'Wrong shape: {S}. Should be a number between 0 and 1.')

	@property
	def grade(self):
		return self.__grade

	@grade.setter
	def grade(self,G):
		self.__grade = G if (isinstance(G, (int))) and (1 <= G <= 3) else print(f'Wrong grade: {R}. Should be 1, 2, 3.')
	# ====================================


	# redefine str for print
	def __str__(self):
		return f"""Armor piece. 
		type: {self.__material}, slot: {self.__slot}, grade: {self.__grade}.
		Ideal: S - {self.__ideal[0]}, P - {self.__ideal[1]}, B - {self.__ideal[2]}.
		Rigidity: {self.__rigidity}.
		Coverage: {self.__coverage}.
		Shape: {self.__shape}."""

	# custom constructor
	@classmethod
	def custom(cls,slot,material,G,Is,Ip,Ib,R,S,C):
		if all([checklist([Is,Ip,Ib]), 
			isinstance(G, (int)), (1 <= G <= 3),
			isinstance(R, (int,float)), (0 <= R <= 1), 
			isinstance(S, (int,float)), (0 <= S <= 1), 
			isinstance(C, (int,float)), (0 <= C <= 1)]):
			newslots = {slot:C}
			newmaterials = {material : [[Is,Ip,Ib],R]}
			return cls(slot,material,L,S,slotsdict=newslots,materialsdict=newmaterials)
			
		else:
			print('One of the parameters are wrong. Setting all to 0.')
			return cls('test','test')

	# used in calculator to check if input is armor piece
	def check(self):
		pass

	# calculate armor class of a piece
	def ac(self):
		return [i*self.__coverage for i in self.__ideal]




class ArmorCalculator:

	def __init__(self):
		self.__pieces = [] # list of all base armor pieces
		self.__layer4 = [] # list of additional armor pieces

	@property
	def pieces(self):
		return self.__pieces

	def list_pieces(self):
		for piece in self.__pieces:
			print(piece)

	# Add armor piece to calculation
	def add_piece(self,piece,layer4:bool = False):
		try:
			piece.check() # check that piece is an object of armor_piece class

#			print(f'adding: {piece}')

			if layer4:
				self.__layer4.append(piece)
			else:
				self.__pieces.append(piece)

		except(AttributeError):
			print("This isn't an object of type armor_piece.")



	def make_armor_set(self, mode):
		modes = ['simple','basic','custom']
		if mode not in modes:
			raise ValueError( f'Forbidden mode. Allowed modes: {', '.join(modes)}.')

		match mode:
			case 'simple':
				# Simple mode allows to choose from the list of prepared sets of armor
				print('Simple mode.')
				sets = {1: ['1: Городская одежда',
						armor_piece('jacket','cloth',slotsdict=extended_slots_1),
						armor_piece('pants','cloth',slotsdict=extended_slots_1),
						armor_piece('boots','leather-s',slotsdict=extended_slots_1)],

						2: ['2: Кожаный доспех',
						armor_piece('pants','leather-s',slotsdict=extended_slots_1),
						armor_piece('jacket','leather-s',slotsdict=extended_slots_1),
						armor_piece('jacket','cloth',slotsdict=extended_slots_1),
						armor_piece('boots','leather-s',slotsdict=extended_slots_1)],

						3: ['3: Броня раннесредневекового рыцаря',
						armor_piece('pants','cloth',slotsdict=extended_slots_1),
						armor_piece('boots','leather-s',slotsdict=extended_slots_1),
						armor_piece('jacket','gambeson',slotsdict=extended_slots_1),
						armor_piece('pants','mail',slotsdict=extended_slots_1),
						armor_piece('jacket','mail',slotsdict=extended_slots_1),
						armor_piece('head','plate')]}
				print(list(sets.keys()))
				print(f'Availible sets: {', '.join([sets[n][0] for n in sets.keys()])}. Please, choose one of them ({', '.join(list(map(str,sets.keys())))}):')
				while True:
					chosen_set = str(input())
					if chosen_set in list(map(str,sets.keys())):
						break
					else:
						print(f'Wrong input. Please, choose one of {', '.join(list(map(str,sets.keys())))}.')

				print(f'You chose {sets[int(chosen_set)][0]}')

#				print(sets[int(chosen_set)][1:])
				for piece in sets[int(chosen_set)][1:]:
					self.add_piece(piece)

			case 'basic':
				print('Basic mode.')
				# Basic mode allows to cuntruct armor sets from given slots and materials
				slots_table = []
				for key, values in basic_slots.items():
					row = [key] + [values]
					slots_table.append(row)
				print('Basic slots availible:')
				print(tabulate(slots_table, headers=['Название','Покрытие'], tablefmt="grid", missingval="-"))
				slots_table_ext = []
				for key, values in extended_slots_1.items():
					row = [key] + [values]
					slots_table_ext.append(row)
				print('Extended slots availible:')
				print(tabulate(slots_table_ext, headers=['Название','Покрытие'], tablefmt="grid", missingval="-"))
				materials_table = []
				for key, values in basic_materials.items():
					row = [key] + values[0] + values[1:]
					materials_table.append(row)
				print('Basic materials availible:')
				print(tabulate(materials_table, headers=['Название','Идеал РКД','Идеал ККД','Идеал ДКД','Жёсткость','Грейд'], tablefmt="grid", missingval="-"))



			case 'custom':
				print('Custom mode. Enjoy experimenting!')



			




	def get_ac(self):
		armor_class = [0,0,0]
		grades = {1:[0,0,0], 2:[0,0,0], 3:[0,0,0]}

		for piece in self.__grade1:
			grades[1] = [x+y for x,y in zip(grades[1],piece.ac())]

		for piece in self.__grade2:
			grades[2] = [x+y for x,y in zip(grades[2],piece.ac())]

		for piece in self.__grade3:
			grades[3] = [x+y for x,y in zip(grades[3],piece.ac())]


		print(grades)
		# Base layers first

		# Slashing ac is calculated on the top grade only:
		#armor_class[0] = grades[3][0] if self.__grade3 else (grades[2][0] if self.__grade2 else grades[1][0] if self.__grade1 else None)
		





		return armor_class



# test
calc = ArmorCalculator()
md = str(input('select mode (simple, basic, custom): '))
calc.make_armor_set(md)

calc.list_pieces()